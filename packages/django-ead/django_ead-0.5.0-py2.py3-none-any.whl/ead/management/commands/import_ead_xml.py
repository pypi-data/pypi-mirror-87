"""Import records from supplied EAD XML files.

Validates imported files against the EAD3 XSD, and also against the
Django models' validators, partly due to small differences between the
two (eg, an empty physfacet is valid in the XML, not in the Django
model) and partly as a sanity check.

"""

import logging
import os.path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from lxml import etree

from controlled_vocabulary.utils import search_term

import reversion

from ...constants import (
    ABBR_ATTRS, ABSTRACT_ATTRS, ACCESSRESTRICT_ATTRS, ACCRUALS_ATTRS,
    ACQINFO_ATTRS, ADDRESS_ATTRS, ADDRESSLINE_ATTRS, AGENCYCODE_ATTRS,
    AGENCYNAME_ATTRS, AGENT_ATTRS, AGENTTYPE_ATTRS, ALTFORMAVAIL_ATTRS,
    APPRAISAL_ATTRS, ARCHDESC_ATTRS, ARRANGEMENT_ATTRS, AUTHOR_ATTRS,
    BIBLIOGRAPHY_ATTRS, BIOGHIST_ATTRS, CITATION_ATTRS, CONTAINER_ATTRS,
    CONTROL_ATTRS, CONTROLACCESS_ATTRS, CONTROLNOTE_ATTRS,
    CONVENTIONDECLARATION_ATTRS, CUSTODHIST_ATTRS, DAO_ATTRS, DAOSET_ATTRS,
    DATERANGE_ATTRS, DATESET_ATTRS, DATESINGLE_ATTRS, DESCRIPTIVENOTE_ATTRS,
    DID_ATTRS, DIDNOTE_ATTRS, DIMENSIONS_ATTRS, EAD_ATTRS, EAD_NS,
    EDITIONSTMT_ATTRS, EVENTDATETIME_ATTRS, EVENTDESCRIPTION_ATTRS,
    EVENTTYPE_ATTRS, FILEDESC_ATTRS, FILEPLAN_ATTRS, FROMTODATE_ATTRS,
    GEOGNAME_ATTRS, HEAD_ATTRS, INDEX_ATTRS, LANGMATERIAL_ATTRS,
    LANGUAGE_ATTRS, LANGUAGEDECLARATION_ATTRS, LANGUAGESET_ATTRS,
    LEGALSTATUS_ATTRS, LOCALCONTROL_ATTRS, LOCALTYPEDECLARATION_ATTRS,
    MAINTENANCEAGENCY_ATTRS, MAINTENANCEEVENT_ATTRS, MAINTENANCEHISTORY_ATTRS,
    MAINTENANCESTATUS_ATTRS, MATERIALSPEC_ATTRS, NAME_ATTRS, NOTESTMT_ATTRS,
    NS_MAP, OBJECTXMLWRAP_ATTRS, ODD_ATTRS, ORIGINALSLOC_ATTRS,
    ORIGINATION_ATTRS, OTHERAGENCYCODE_ATTRS, OTHERFINDAID_ATTRS,
    OTHERRECORDID_ATTRS, PART_ATTRS, PHYSDESC_ATTRS, PHYSDESCSET_ATTRS,
    PHYSDESCSTRUCTURED_ATTRS, PHYSFACET_ATTRS, PHYSLOC_ATTRS, PHYSTECH_ATTRS,
    PREFERCITE_ATTRS, PROCESSINFO_ATTRS, PUBLICATIONSTATUS_ATTRS,
    PUBLICATIONSTMT_ATTRS, QUANTITY_ATTRS, RECORDID_ATTRS,
    RELATEDMATERIAL_ATTRS, RELATION_ATTRS, RELATIONENTRY_ATTRS,
    RELATIONS_ATTRS, REPOSITORY_ATTRS, REPRESENTATION_ATTRS,
    RIGHTSDECLARATION_ATTRS, SCOPECONTENT_ATTRS, SCRIPT_ATTRS,
    SEPARATEDMATERIAL_ATTRS, SERIESSTMT_ATTRS, SOURCE_ATTRS, SOURCEENTRY_ATTRS,
    SOURCES_ATTRS, SPONSOR_ATTRS, SUBTITLE_ATTRS, TERM_ATTRS,
    TITLEPROPER_ATTRS, TITLESTMT_ATTRS, UNITDATE_ATTRS,
    UNITDATESTRUCTURED_ATTRS, UNITID_ATTRS, UNITTITLE_ATTRS, UNITTYPE_ATTRS,
    USERESTRICT_ATTRS)
from ...models import (
    Abstract, AccessRestrict, Accruals, AcqInfo, AgencyName, AltFormAvail,
    Appraisal, Arrangement, Author, Bibliography, BiogHist, Container,
    ControlAccess, ControlNote, ConventionDeclaration, CorpName, CorpNamePart,
    CustodHist, DAOSet, DAOSetDAO, DIdDAO, DIdNote, DIdPhysDescStructured,
    DIdPhysDescStructuredDimensions, DIdPhysDescStructuredPhysFacet, EAD,
    EventDescription, FamName, FamNamePart, FilePlan, Index, LangMaterial,
    LangMaterialLanguage, LanguageDeclaration, LanguageSet,
    LanguageSetLanguage, LanguageSetScript, LegalStatus, LocalControl,
    LocalTypeDeclaration, MaintenanceEvent, MaterialSpec, Name, NamePart, ODD,
    OriginalsLoc, Origination, OtherAgencyCode, OtherFindAid, OtherRecordID,
    PersName, PersNamePart, PhysDesc, PhysDescSet,
    PhysDescSetPhysDescStructured, PhysDescSetPhyDescStructuredDimensions,
    PhysDescSetPhysDescStructuredPhysFacet, PhysLoc, PhysTech, PreferCite,
    ProcessInfo, RelatedMaterial, Relation, RelationDateRange,
    RelationDateSingle, RelationEntry, Repository, RepositoryAddressLine,
    Representation, RightsDeclaration, ScopeContent, SeparatedMaterial, Source,
    SourceEntry, Sponsor, Subtitle, TitleProper, UnitDate, UnitDateStructured,
    UnitDateStructuredDateRange, UnitDateStructuredDateSingle, UnitId,
    UnitTitle, UseRestrict)


# Parser options.
HELP = ('Import archival data from EAC XML files. Creates initial revisions '
        'on successful import.')
PATHS_HELP = 'Path to EAD XML file to import.'

EAD_XSD_FILENAME = 'ead3.xsd'

# Logging and error messages.
EMPTY_NAME_MSG = 'Name to be imported within file at {} is empty.'
NO_MATCHING_LANGUAGE_MSG = 'Could not find language matching code "{}".'
NO_MATCHING_SCRIPT_MSG = 'Could not find script matching code "{}".'
NOT_WELL_FORMED_XML_MSG = (
    'Document "{}" is either not well-formed XML or is invalid: {}')
RECORD_EXISTS_MSG = (
    'Document "{}" has recordid "{}" that already exists, sourced from {}')
UNSUPPORTED_RECORD_LEVEL_MSG = (
    'Document "{}" specifies unsupported archdesc/@level "{}"')


def import_attrs(source, attrs, dest, prefix=''):
    """Add any of `attrs` on `source` to `dest`, appending `prefix` to the
    fieldname."""
    for attr in attrs:
        attr_value = source.get(attr)
        if attr == 'id':
            attr = 'ead_id'
        if attr_value is not None:
            if attr == 'lang':
                lang_code = attr_value
                attr_value = search_term('iso639-2', lang_code, exact=True)
                if attr_value is None:
                    raise CommandError(NO_MATCHING_LANGUAGE_MSG.format(
                        lang_code))
            elif attr == 'script':
                script_code = attr_value
                attr_value = search_term('iso15924', script_code, exact=True)
                if attr_value is None:
                    raise CommandError(NO_MATCHING_SCRIPT_MSG.format(
                        script_code))
            elif attr in ('approximate', 'parallel'):
                # BooleanFields.
                if attr_value == 'true':
                    attr_value = True
                else:
                    attr_value = False
            setattr(dest, prefix + attr, attr_value)


def serialise(element):
    """Return `element` serialised, minus the tags for `element`."""
    parts = []
    parts.append(element.text or '')
    for child in element:
        parts.append(etree.tostring(
            child, encoding='unicode', xml_declaration=False))
    return ''.join(parts)


def xpath(source, expression):
    return source.xpath(expression, namespaces=NS_MAP)


class Command(BaseCommand):

    help = HELP
    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument('paths', help=PATHS_HELP, metavar='FILE',
                            nargs='+', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        self._record_ids = {}
        xsd = self._get_xsd()
        parser = etree.XMLParser(ns_clean=True, remove_blank_text=True,
                                 schema=xsd)
        for path in options['paths']:
            self._path = os.path.abspath(path)
            self._handle_path(self._path, parser)

    def _get_xsd(self):
        xsd_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                EAD_XSD_FILENAME)
        xsd_doc = etree.parse(xsd_path)
        return etree.XMLSchema(xsd_doc)

    def _handle_path(self, path, parser):
        try:
            tree = etree.parse(path, parser=parser)
        except etree.XMLSyntaxError as e:
            raise CommandError(NOT_WELL_FORMED_XML_MSG.format(path, e))
        ead = tree.getroot()
        try:
            self.stdout.write('Importing file at {}.'.format(path))
            self._import_ead(ead)
        except Exception as e:
            self.stdout.write('Problem occurred importing file at {}.'.format(
                path))
            raise e

    def _import_abbr(self, abbr, parent_obj):
        """abbr may occur as the child of many elements; this method is only
        for abbr as a child of elements where it may occur only once."""
        parent_obj.abbr = abbr.text
        import_attrs(abbr, ABBR_ATTRS, parent_obj, 'abbr_')
        parent_obj.save()

    def _import_abstract(self, abstract, ead_obj):
        abstract_obj = Abstract(did=ead_obj, abstract=serialise(abstract))
        import_attrs(abstract, ABSTRACT_ATTRS, abstract_obj)
        abstract_obj.full_clean()
        abstract_obj.save()

    def _import_accessrestrict(self, accessrestrict, ead_obj):
        accessrestrict_obj = AccessRestrict(
            archdesc=ead_obj, accessrestrict=serialise(accessrestrict))
        import_attrs(accessrestrict, ACCESSRESTRICT_ATTRS, accessrestrict_obj)
        accessrestrict_obj.full_clean()
        accessrestrict_obj.save()

    def _import_accruals(self, accruals, ead_obj):
        accruals_obj = Accruals(archdesc=ead_obj, accruals=serialise(accruals))
        import_attrs(accruals, ACCRUALS_ATTRS, accruals_obj)
        accruals_obj.full_clean()
        accruals_obj.save()

    def _import_acqinfo(self, acqinfo, ead_obj):
        acqinfo_obj = AcqInfo(archdesc=ead_obj, acqinfo=serialise(acqinfo))
        import_attrs(acqinfo, ACQINFO_ATTRS, acqinfo_obj)
        acqinfo_obj.full_clean()
        acqinfo_obj.save()

    def _import_address(self, address, repository_obj):
        import_attrs(address, ADDRESS_ATTRS, repository_obj, 'address_')
        repository_obj.full_clean()
        repository_obj.save()
        for addressline in xpath(address, 'e:addressline'):
            self._import_addressline(addressline, repository_obj)

    def _import_addressline(self, addressline, repository_obj):
        addressline_obj = RepositoryAddressLine(
            address=repository_obj, addressline=serialise(addressline))
        import_attrs(addressline, ADDRESSLINE_ATTRS, addressline_obj)
        addressline_obj.full_clean()
        addressline_obj.save()

    def _import_agencycode(self, agencycode, ead_obj):
        import_attrs(agencycode, AGENCYCODE_ATTRS, ead_obj, 'agencycode_')
        ead_obj.agencycode = agencycode.text

    def _import_agencyname(self, agencyname, ead_obj):
        agencyname_obj = AgencyName(
            maintenanceagency=ead_obj, agencyname=agencyname.text)
        import_attrs(agencyname, AGENCYNAME_ATTRS, agencyname_obj)
        agencyname_obj.full_clean()
        agencyname_obj.save()

    def _import_agent(self, agent, maintenanceevent_obj):
        import_attrs(agent, AGENT_ATTRS, maintenanceevent_obj, 'agent_')
        if agent.text:
            maintenanceevent_obj.agent = agent.text

    def _import_agenttype(self, agenttype, maintenanceevent_obj):
        import_attrs(agenttype, AGENTTYPE_ATTRS, maintenanceevent_obj,
                     'agenttype_')
        if agenttype.text:
            maintenanceevent_obj.agenttype = agenttype.text

    def _import_altformavail(self, altformavail, ead_obj):
        altformavail_obj = AltFormAvail(
            archdesc=ead_obj, altformavail=serialise(altformavail))
        import_attrs(altformavail, ALTFORMAVAIL_ATTRS, altformavail_obj)
        altformavail_obj.full_clean()
        altformavail_obj.save()

    def _import_appraisal(self, appraisal, ead_obj):
        appraisal_obj = Appraisal(
            archdesc=ead_obj, appraisal=serialise(appraisal))
        import_attrs(appraisal, APPRAISAL_ATTRS, appraisal_obj)
        appraisal_obj.full_clean()
        appraisal_obj.save()

    def _import_archdesc(self, archdesc, ead_obj):
        import_attrs(archdesc, ARCHDESC_ATTRS, ead_obj, 'archdesc_')
        did = archdesc[0]
        self._import_did(did, ead_obj)
        for accessrestrict in xpath(archdesc, 'e:accessrestrict'):
            self._import_accessrestrict(accessrestrict, ead_obj)
        for accruals in xpath(archdesc, 'e:accruals'):
            self._import_accruals(accruals, ead_obj)
        for acqinfo in xpath(archdesc, 'e:acqinfo'):
            self._import_acqinfo(acqinfo, ead_obj)
        for altformavail in xpath(archdesc, 'e:altformavail'):
            self._import_altformavail(altformavail, ead_obj)
        for appraisal in xpath(archdesc, 'e:appraisal'):
            self._import_appraisal(appraisal, ead_obj)
        for arrangement in xpath(archdesc, 'e:arrangement'):
            self._import_arrangement(arrangement, ead_obj)
        for bibliography in xpath(archdesc, 'e:bibliography'):
            self._import_bibliography(bibliography, ead_obj)
        for bioghist in xpath(archdesc, 'e:bioghist'):
            self._import_bioghist(bioghist, ead_obj)
        for controlaccess in xpath(archdesc, 'e:controlaccess'):
            self._import_controlaccess(controlaccess, ead_obj)
        for custodhist in xpath(archdesc, 'e:custodhist'):
            self._import_custodhist(custodhist, ead_obj)
        for fileplan in xpath(archdesc, 'e:fileplan'):
            self._import_fileplan(fileplan, ead_obj)
        for index in xpath(archdesc, 'e:index'):
            self._import_index(index, ead_obj)
        for legalstatus in xpath(archdesc, 'e:legalstatus'):
            self._import_legalstatus(legalstatus, ead_obj)
        for odd in xpath(archdesc, 'e:odd'):
            self._import_odd(odd, ead_obj)
        for originalsloc in xpath(archdesc, 'e:originalsloc'):
            self._import_originalsloc(originalsloc, ead_obj)
        for otherfindaid in xpath(archdesc, 'e:otherfindaid'):
            self._import_otherfindaid(otherfindaid, ead_obj)
        for phystech in xpath(archdesc, 'e:phystech'):
            self._import_phystech(phystech, ead_obj)
        for prefercite in xpath(archdesc, 'e:prefercite'):
            self._import_prefercite(prefercite, ead_obj)
        for processinfo in xpath(archdesc, 'e:processinfo'):
            self._import_processinfo(processinfo, ead_obj)
        for relatedmaterial in xpath(archdesc, 'e:relatedmaterial'):
            self._import_relatedmaterial(relatedmaterial, ead_obj)
        for relations in xpath(archdesc, 'e:relations'):
            self._import_relations(relations, ead_obj)
        for scopecontent in xpath(archdesc, 'e:scopecontent'):
            self._import_scopecontent(scopecontent, ead_obj)
        for separatedmaterial in xpath(archdesc, 'e:separatedmaterial'):
            self._import_separatedmaterial(separatedmaterial, ead_obj)
        for userestrict in xpath(archdesc, 'e:userestrict'):
            self._import_userestrict(userestrict, ead_obj)

    def _import_arrangement(self, arrangement, ead_obj):
        arrangement_obj = Arrangement(
            archdesc=ead_obj, arrangement=serialise(arrangement))
        import_attrs(arrangement, ARRANGEMENT_ATTRS, arrangement_obj)
        arrangement_obj.full_clean()
        arrangement_obj.save()

    def _import_author(self, author, ead_obj):
        author_obj = Author(titlestmt=ead_obj, author=serialise(author))
        import_attrs(author, AUTHOR_ATTRS, author_obj)
        author_obj.full_clean()
        author_obj.save()

    def _import_bibliography(self, bibliography, ead_obj):
        bibliography_obj = Bibliography(
            archdesc=ead_obj, bibliography=serialise(bibliography))
        import_attrs(bibliography, BIBLIOGRAPHY_ATTRS, bibliography_obj)
        bibliography_obj.full_clean()
        bibliography_obj.save()

    def _import_bioghist(self, bioghist, ead_obj):
        bioghist_obj = BiogHist(archdesc=ead_obj, bioghist=serialise(bioghist))
        import_attrs(bioghist, BIOGHIST_ATTRS, bioghist_obj)
        bioghist_obj.full_clean()
        bioghist_obj.save()

    def _import_citation(self, citation, parent_obj):
        parent_obj.citation = serialise(citation)
        import_attrs(citation, CITATION_ATTRS, parent_obj, 'citation_')

    def _import_container(self, container, ead_obj):
        container_obj = Container(did=ead_obj, container=serialise(container))
        import_attrs(container, CONTAINER_ATTRS, container_obj)
        container_obj.full_clean()
        container_obj.save()
        return container_obj

    def _import_container_parents(self, container, container_obj, ead_obj):
        for idref in container.get('parent', '').split():
            parent_obj = Container.objects.get(did=ead_obj, ead_id=idref)
            container_obj.parents.add(parent_obj)

    def _import_control(self, control, ead_obj):
        import_attrs(control, CONTROL_ATTRS, ead_obj, 'control_')
        self._import_recordid(control[0], ead_obj)
        ead_obj.save()
        for otherrecordid in xpath(control, 'e:otherrecordid'):
            self._import_otherrecordid(otherrecordid, ead_obj)
        for representation in xpath(control, 'e:representation'):
            self._import_representation(representation, ead_obj)
        filedesc = xpath(control, 'e:filedesc')[0]
        self._import_filedesc(filedesc, ead_obj)
        maintenancestatus = xpath(control, 'e:maintenancestatus')[0]
        self._import_maintenancestatus(maintenancestatus, ead_obj)
        for publicationstatus in xpath(control, 'e:publicationstatus'):
            self._import_publicationstatus(publicationstatus, ead_obj)
        maintenanceagency = xpath(control, 'e:maintenanceagency')[0]
        self._import_maintenanceagency(maintenanceagency, ead_obj)
        for languagedeclaration in xpath(control, 'e:languagedeclaration'):
            self._import_languagedeclaration(languagedeclaration, ead_obj)
        for conventiondeclaration in xpath(control, 'e:conventiondeclaration'):
            self._import_conventiondeclaration(conventiondeclaration, ead_obj)
        for rightsdeclaration in xpath(control, 'e:rightsdeclaration'):
            self._import_rightsdeclaration(rightsdeclaration, ead_obj)
        for localtypedeclaration in xpath(control, 'e:localtypedeclaration'):
            self._import_localtypedeclaration(localtypedeclaration, ead_obj)
        for localcontrol in xpath(control, 'e:localcontrol'):
            self._import_localcontrol(localcontrol, ead_obj)
        maintenancehistory = xpath(control, 'e:maintenancehistory')[0]
        self._import_maintenancehistory(maintenancehistory, ead_obj)
        for sources in xpath(control, 'e:sources'):
            self._import_sources(sources, ead_obj)

    def _import_controlaccess(self, controlaccess, ead_obj):
        controlaccess_obj = ControlAccess(
            archdesc=ead_obj, controlaccess=serialise(controlaccess))
        import_attrs(controlaccess, CONTROLACCESS_ATTRS, controlaccess_obj)
        controlaccess_obj.full_clean()
        controlaccess_obj.save()

    def _import_controlnote(self, controlnote, ead_obj):
        controlnote_obj = ControlNote(
            notestmt=ead_obj, controlnote=serialise(controlnote))
        import_attrs(controlnote, CONTROLNOTE_ATTRS, controlnote_obj)
        controlnote_obj.full_clean()
        controlnote_obj.save()

    def _import_conventiondeclaration(self, conventiondeclaration, ead_obj):
        conventiondeclaration_obj = ConventionDeclaration(
            control=ead_obj)
        import_attrs(conventiondeclaration, CONVENTIONDECLARATION_ATTRS,
                     conventiondeclaration_obj)
        for abbr in xpath(conventiondeclaration, 'e:abbr'):
            self._import_abbr(abbr, conventiondeclaration_obj)
        for citation in xpath(conventiondeclaration, 'e:citation'):
            self._import_citation(citation, conventiondeclaration_obj)
        for descriptivenote in xpath(
                conventiondeclaration, 'e:descriptivenote'):
            self._import_descriptivenote(
                descriptivenote, conventiondeclaration_obj)
        conventiondeclaration_obj.full_clean()
        conventiondeclaration_obj.save()

    def _import_custodhist(self, custodhist, ead_obj):
        custodhist_obj = CustodHist(
            archdesc=ead_obj, custodhist=serialise(custodhist))
        import_attrs(custodhist, CUSTODHIST_ATTRS, custodhist_obj)
        custodhist_obj.full_clean()
        custodhist_obj.save()

    def _import_dao(self, dao, parent_obj):
        if dao.getparent().tag == EAD_NS + 'did':
            dao_model = DIdDAO
        else:
            dao_model = DAOSetDAO
        dao_obj = dao_model(parent=parent_obj)
        import_attrs(dao, DAO_ATTRS, dao_obj)
        for descriptivenote in xpath(dao, 'e:descriptivenote'):
            self._import_descriptivenote(descriptivenote, dao_obj)
        dao_obj.full_clean()
        dao_obj.save()

    def _import_daoset(self, daoset, ead_obj):
        daoset_obj = DAOSet(did=ead_obj)
        import_attrs(daoset, DAOSET_ATTRS, daoset_obj)
        for descriptivenote in xpath(daoset, 'e:descriptivenote'):
            self._import_descriptivenote(descriptivenote, daoset_obj)
        daoset_obj.full_clean()
        daoset_obj.save()
        for dao in xpath(daoset, 'e:dao'):
            self._import_dao(dao, daoset_obj)

    def _import_daterange(self, daterange, parent_obj, daterange_model):
        daterange_obj = daterange_model(parent=parent_obj)
        import_attrs(daterange, DATERANGE_ATTRS, daterange_obj)
        for fromdate in xpath(daterange, 'e:fromdate'):
            self._import_fromtodate(fromdate, daterange_obj, 'fromdate')
        for todate in xpath(daterange, 'e:todate'):
            self._import_fromtodate(todate, daterange_obj, 'todate')
        daterange_obj.full_clean()
        daterange_obj.save()

    def _import_datesingle(self, datesingle, parent_obj, datesingle_model):
        datesingle_obj = datesingle_model(parent=parent_obj)
        import_attrs(datesingle, DATESINGLE_ATTRS, datesingle_obj)
        if datesingle.text or len(datesingle):
            datesingle_obj.datesingle = serialise(datesingle)
        datesingle_obj.full_clean()
        datesingle_obj.save()

    def _import_descriptivenote(self, descriptivenote, parent_obj, prefix=''):
        setattr(parent_obj, prefix + 'descriptivenote', serialise(
            descriptivenote))
        import_attrs(descriptivenote, DESCRIPTIVENOTE_ATTRS, parent_obj,
                     prefix + 'descriptivenote_')

    def _import_did(self, did, ead_obj):
        import_attrs(did, DID_ATTRS, ead_obj, 'did_')
        for head in xpath(did, 'e:head'):
            self._import_head(head, ead_obj, 'did_')
        for abstract in xpath(did, 'e:abstract'):
            self._import_abstract(abstract, ead_obj)
        containers = xpath(did, 'e:container')
        container_objs = []
        for container in containers:
            container_objs.append(self._import_container(container, ead_obj))
        # container @parent requires processing after all Containers
        # have been created.
        for container, container_obj in zip(containers, container_objs):
            self._import_container_parents(container, container_obj, ead_obj)
        for dao in xpath(did, 'e:dao'):
            self._import_dao(dao, ead_obj)
        for daoset in xpath(did, 'e:daoset'):
            self._import_daoset(daoset, ead_obj)
        for didnote in xpath(did, 'e:didnote'):
            self._import_didnote(didnote, ead_obj)
        for langmaterial in xpath(did, 'e:langmaterial'):
            self._import_langmaterial(langmaterial, ead_obj)
        for materialspec in xpath(did, 'e:materialspec'):
            self._import_materialspec(materialspec, ead_obj)
        for origination in xpath(did, 'e:origination'):
            self._import_origination(origination, ead_obj)
        for physdesc in xpath(did, 'e:physdesc'):
            self._import_physdesc(physdesc, ead_obj)
        for physdescset in xpath(did, 'e:physdescset'):
            self._import_physdescset(physdescset, ead_obj)
        for physdescstructured in xpath(did, 'e:physdescstructured'):
            self._import_physdescstructured(physdescstructured, ead_obj)
        physlocs = xpath(did, 'e:physloc')
        physloc_objs = []
        for physloc in physlocs:
            physloc_objs.append(self._import_physloc(physloc, ead_obj))
        # physloc @parent requires processing after all
        # PhysLocs have been created.
        for physloc, physloc_obj in zip(physlocs, physloc_objs):
            self._import_physloc_parents(physloc, physloc_obj, ead_obj)
        for repository in xpath(did, 'e:repository'):
            self._import_repository(repository, ead_obj)
        for unitdate in xpath(did, 'e:unitdate'):
            self._import_unitdate(unitdate, ead_obj)
        for unitdatestructured in xpath(did, 'e:unitdatestructured'):
            self._import_unitdatestructured(unitdatestructured, ead_obj)
        for unitid in xpath(did, 'e:unitid'):
            self._import_unitid(unitid, ead_obj)
        for unittitle in xpath(did, 'e:unittitle'):
            self._import_unittitle(unittitle, ead_obj)

    def _import_didnote(self, didnote, ead_obj):
        didnote_obj = DIdNote(did=ead_obj, didnote=serialise(didnote))
        import_attrs(didnote, DIDNOTE_ATTRS, didnote_obj)
        didnote_obj.full_clean()
        didnote_obj.save()

    def _import_dimensions(self, dimensions, pds_obj, dimensions_model):
        dimensions_obj = dimensions_model(
            physdescstructured=pds_obj, dimensions=serialise(dimensions))
        import_attrs(dimensions, DIMENSIONS_ATTRS, dimensions_obj)
        dimensions_obj.full_clean()
        dimensions_obj.save()

    def _import_ead(self, ead):
        """Create and return an EAD object from the data in `ead`.

        The record is saved. If a record with the same record_id
        already exists, an exception is raised.

        """
        recordid = xpath(ead, 'e:control/e:recordid')[0].text
        try:
            ead_obj = EAD.objects.get(recordid=recordid)
            source = self._record_ids.get(recordid, 'an earlier import')
            raise CommandError(RECORD_EXISTS_MSG.format(
                self._path, recordid, source))
        except EAD.DoesNotExist:
            pass
        self._record_ids[recordid] = self._path
        with reversion.create_revision():
            ead_obj = EAD()
            import_attrs(ead, EAD_ATTRS, ead_obj)
            self._import_control(ead[0], ead_obj)
            self._import_archdesc(ead[1], ead_obj)
            ead_obj.full_clean()
            ead_obj.save()
            reversion.set_comment('Created record from EAD3 XML.')
        return ead_obj

    def _import_editionstmt(self, editionstmt, ead_obj):
        import_attrs(editionstmt, EDITIONSTMT_ATTRS, ead_obj,
                     'editionstmt_')
        ead_obj.editionstmt = serialise(editionstmt)

    def _import_eventdatetime(self, eventdatetime, maintenanceevent_obj):
        import_attrs(eventdatetime, EVENTDATETIME_ATTRS, maintenanceevent_obj,
                     'eventdatetime_')
        if eventdatetime.text:
            maintenanceevent_obj.eventdatetime = eventdatetime.text

    def _import_eventdescription(self, eventdescription, maintenanceevent_obj):
        eventdescription_obj = EventDescription(
            maintenanceevent=maintenanceevent_obj)
        import_attrs(eventdescription, EVENTDESCRIPTION_ATTRS,
                     eventdescription_obj)
        eventdescription_obj.eventdescription = eventdescription.text
        eventdescription_obj.full_clean()
        eventdescription_obj.save()

    def _import_eventtype(self, eventtype, maintenanceevent_obj):
        import_attrs(eventtype, EVENTTYPE_ATTRS, maintenanceevent_obj,
                     'eventtype_')
        if eventtype.text:
            maintenanceevent_obj.eventtype = eventtype.text

    def _import_filedesc(self, filedesc, ead_obj):
        import_attrs(filedesc, FILEDESC_ATTRS, ead_obj, 'filedesc_')
        self._import_titlestmt(xpath(filedesc, 'e:titlestmt')[0], ead_obj)
        for editionstmt in xpath(filedesc, 'e:editionstmt'):
            self._import_editionstmt(editionstmt, ead_obj)
        for publicationstmt in xpath(filedesc, 'e:publicationstmt'):
            self._import_publicationstmt(publicationstmt, ead_obj)
        for seriesstmt in xpath(filedesc, 'e:seriesstmt'):
            self._import_seriesstmt(seriesstmt, ead_obj)
        for notestmt in xpath(filedesc, 'e:notestmt'):
            self._import_notestmt(notestmt, ead_obj)

    def _import_fileplan(self, fileplan, ead_obj):
        fileplan_obj = FilePlan(archdesc=ead_obj, fileplan=serialise(fileplan))
        import_attrs(fileplan, FILEPLAN_ATTRS, fileplan_obj)
        fileplan_obj.full_clean()
        fileplan_obj.save()

    def _import_fromtodate(self, fromtodate, daterange_obj, field_name):
        # Due to the usefulness of some attributes on fromdate/todate
        # for processing, store the attributes in model fields, along
        # with the serialised element.
        if fromtodate.text or len(fromtodate):
            setattr(daterange_obj, field_name, serialise(fromtodate))
        import_attrs(fromtodate, FROMTODATE_ATTRS, daterange_obj,
                     field_name + '_')

    def _import_geogname(self, geogname, relation_obj):
        relation_obj.geogname = serialise(geogname)
        import_attrs(geogname, GEOGNAME_ATTRS, relation_obj, 'geogname_')

    def _import_head(self, head, parent_obj, prefix=''):
        setattr(parent_obj, prefix + 'head', serialise(head))
        import_attrs(head, HEAD_ATTRS, parent_obj, prefix + 'head_')

    def _import_index(self, index, ead_obj):
        index_obj = Index(archdesc=ead_obj, index=serialise(index))
        import_attrs(index, INDEX_ATTRS, index_obj)
        index_obj.full_clean()
        index_obj.save()

    def _import_langmaterial(self, langmaterial, ead_obj):
        langmaterial_obj = LangMaterial(did=ead_obj)
        import_attrs(langmaterial, LANGMATERIAL_ATTRS, langmaterial_obj)
        for descriptivenote in xpath(langmaterial, 'e:descriptivenote'):
            self._import_descriptivenote(descriptivenote, langmaterial_obj)
        langmaterial_obj.full_clean()
        langmaterial_obj.save()
        for language in xpath(langmaterial, 'e:language'):
            self._import_language(
                language, langmaterial_obj, LangMaterialLanguage)
        for languageset in xpath(langmaterial, 'e:languageset'):
            self._import_languageset(languageset, langmaterial_obj)

    def _import_language(self, language, parent_obj, language_model):
        language_obj = language_model(parent=parent_obj)
        import_attrs(language, LANGUAGE_ATTRS, language_obj)
        langcode = language.get('langcode')
        if langcode:
            langcode_obj = search_term('iso639-2', langcode)
            language_obj.langcode = langcode_obj
        language_obj.language = language.text
        language_obj.full_clean()
        language_obj.save()

    def _import_languagedeclaration(self, ld, ead_obj):
        # Cheat by looking for an existing LanguageDeclaration that
        # shares only language code and script code, ignoring all
        # other fields.
        language = ld[0]
        script = ld[1]
        langcode = search_term('iso639-2', language.get('langcode'))
        scriptcode = search_term('iso15924', script.get('scriptcode'))
        try:
            ld_obj = LanguageDeclaration.objects.get(
                language_langcode=langcode, script_el_scriptcode=scriptcode)
        except LanguageDeclaration.DoesNotExist:
            ld_obj = LanguageDeclaration()
            import_attrs(ld, LANGUAGEDECLARATION_ATTRS, ld_obj)
            import_attrs(language, LANGUAGE_ATTRS, ld_obj, 'language_')
            import_attrs(script, SCRIPT_ATTRS, ld_obj, 'script_el_')
            ld_obj.language = language.text
            ld_obj.language_langcode = langcode
            ld_obj.script_el = script.text
            ld_obj.script_el_scriptcode = scriptcode
            for descriptivenote in xpath(ld, 'e:descriptivenote'):
                self._import_descriptivenote(descriptivenote, ld_obj)
            ld_obj.full_clean()
            ld_obj.save()
        ead_obj.languagedeclarations.add(ld_obj)

    def _import_languageset(self, languageset, langmaterial_obj):
        languageset_obj = LanguageSet(langmaterial=langmaterial_obj)
        import_attrs(languageset, LANGUAGESET_ATTRS, languageset_obj)
        for descriptivenote in xpath(languageset, 'e:descriptivenote'):
            self._import_descriptivenote(descriptivenote, languageset_obj)
        languageset_obj.full_clean()
        languageset_obj.save()
        for language in xpath(languageset, 'e:language'):
            self._import_language(
                language, languageset_obj, LanguageSetLanguage)
        for script in xpath(languageset, 'e:script'):
            self._import_script(script, languageset_obj)

    def _import_legalstatus(self, legalstatus, ead_obj):
        legalstatus_obj = LegalStatus(
            archdesc=ead_obj, legalstatus=serialise(legalstatus))
        import_attrs(legalstatus, LEGALSTATUS_ATTRS, legalstatus_obj)
        legalstatus_obj.full_clean()
        legalstatus_obj.save()

    def _import_localcontrol(self, localcontrol, ead_obj):
        localcontrol_obj = LocalControl(control=ead_obj)
        import_attrs(localcontrol, LOCALCONTROL_ATTRS, localcontrol_obj)
        for term in xpath(localcontrol, 'e:term'):
            self._import_term(term, localcontrol_obj)
        for daterange in xpath(localcontrol, 'e:daterange'):
            import_attrs(daterange, DATERANGE_ATTRS, localcontrol_obj,
                         'daterange_')
            for fromdate in xpath(daterange, 'e:fromdate'):
                self._import_fromtodate(fromdate, localcontrol_obj, 'fromdate')
            for todate in xpath(daterange, 'e:todate'):
                self._import_fromtodate(todate, localcontrol_obj, 'todate')
        for datesingle in xpath(localcontrol, 'e:datesingle'):
            import_attrs(datesingle, DATESINGLE_ATTRS, localcontrol_obj,
                         'datesingle_')
            if datesingle.text or len(datesingle):
                localcontrol_obj.datesingle = serialise(datesingle)
        localcontrol_obj.full_clean()
        localcontrol_obj.save()

    def _import_localtypedeclaration(self, ltd, ead_obj):
        ltd_obj = LocalTypeDeclaration(control=ead_obj)
        import_attrs(ltd, LOCALTYPEDECLARATION_ATTRS, ltd_obj)
        for abbr in xpath(ltd, 'e:abbr'):
            self._import_abbr(abbr, ltd_obj)
        for citation in xpath(ltd, 'e:citation'):
            self._import_citation(citation, ltd_obj)
        for descriptivenote in xpath(ltd, 'e:descriptivenote'):
            self._import_descriptivenote(descriptivenote, ltd_obj)
        ltd_obj.full_clean()
        ltd_obj.save()

    def _import_maintenanceagency(self, maintenanceagency, ead_obj):
        import_attrs(maintenanceagency, MAINTENANCEAGENCY_ATTRS, ead_obj,
                     'maintenanceagency_')
        for agencycode in xpath(maintenanceagency, 'e:agencycode'):
            self._import_agencycode(agencycode, ead_obj)
        for otheragencycode in xpath(maintenanceagency, 'e:otheragencycode'):
            self._import_otheragencycode(otheragencycode, ead_obj)
        for agencyname in xpath(maintenanceagency, 'e:agencyname'):
            self._import_agencyname(agencyname, ead_obj)
        for descriptivenote in xpath(maintenanceagency, 'e:descriptivenote'):
            self._import_descriptivenote(
                descriptivenote, ead_obj, 'maintenanceagency_')

    def _import_maintenanceevent(self, maintenanceevent, ead_obj):
        maintenanceevent_obj = MaintenanceEvent(maintenancehistory=ead_obj)
        import_attrs(maintenanceevent, MAINTENANCEEVENT_ATTRS,
                     maintenanceevent_obj)
        self._import_eventtype(maintenanceevent[0], maintenanceevent_obj)
        eventdatetime = maintenanceevent[1]
        self._import_eventdatetime(eventdatetime, maintenanceevent_obj)
        agenttype = maintenanceevent[2]
        self._import_agenttype(agenttype, maintenanceevent_obj)
        agent = maintenanceevent[3]
        self._import_agent(agent, maintenanceevent_obj)
        maintenanceevent_obj.full_clean()
        maintenanceevent_obj.save()
        for eventdescription in maintenanceevent[4:]:
            self._import_eventdescription(
                eventdescription, maintenanceevent_obj)

    def _import_maintenancehistory(self, maintenancehistory, ead_obj):
        import_attrs(maintenancehistory, MAINTENANCEHISTORY_ATTRS, ead_obj,
                     'maintenancehistory_')
        for maintenanceevent in maintenancehistory:
            self._import_maintenanceevent(maintenanceevent, ead_obj)

    def _import_maintenancestatus(self, maintenancestatus, ead_obj):
        import_attrs(maintenancestatus, MAINTENANCESTATUS_ATTRS, ead_obj,
                     'maintenancestatus_')
        if maintenancestatus.text:
            ead_obj.maintenancestatus = maintenancestatus.text

    def _import_materialspec(self, materialspec, ead_obj):
        materialspec_obj = MaterialSpec(
            did=ead_obj, materialspec=serialise(materialspec))
        import_attrs(materialspec, MATERIALSPEC_ATTRS, materialspec_obj)
        materialspec_obj.full_clean()
        materialspec_obj.save()

    def _import_name(self, name, name_model, part_model):
        """Import name from `name` element, using `name_model` and
        `part_model`, and return it. Return an existing name if one
        matches."""
        assembled_name = ''.join(xpath(name, 'e:part//text()'))
        if not assembled_name:
            raise CommandError(EMPTY_NAME_MSG.format(self._path))
        try:
            name_obj = name_model.objects.get(assembled_name=assembled_name)
        except name_model.DoesNotExist:
            name_obj = name_model(assembled_name=assembled_name)
            import_attrs(name, NAME_ATTRS, name_obj)
            name_obj.full_clean()
            name_obj.save()
            for idx, part in enumerate(name):
                self._import_part(part, name_obj, part_model, idx)
            name_obj.full_clean()
            name_obj.save()  # To set the assembled_name from the parts.
        return name_obj

    def _import_notestmt(self, notestmt, ead_obj):
        import_attrs(notestmt, NOTESTMT_ATTRS, ead_obj, 'notestmt_')
        for controlnote in notestmt:
            self._import_controlnote(controlnote, ead_obj)

    def _import_objectxmlwrap(self, objectxmlwrap, parent_obj):
        import_attrs(objectxmlwrap, OBJECTXMLWRAP_ATTRS, parent_obj,
                     'objectxmlwrap_')
        parent_obj.objectxmlwrap = serialise(objectxmlwrap)

    def _import_odd(self, odd, ead_obj):
        odd_obj = ODD(archdesc=ead_obj, odd=serialise(odd))
        import_attrs(odd, ODD_ATTRS, odd_obj)
        odd_obj.full_clean()
        odd_obj.save()

    def _import_originalsloc(self, originalsloc, ead_obj):
        originalsloc_obj = OriginalsLoc(
            archdesc=ead_obj, originalsloc=serialise(originalsloc))
        import_attrs(originalsloc, ORIGINALSLOC_ATTRS, originalsloc_obj)
        originalsloc_obj.full_clean()
        originalsloc_obj.save()

    def _import_origination(self, origination, ead_obj):
        origination_obj = Origination(did=ead_obj)
        import_attrs(origination, ORIGINATION_ATTRS, origination_obj)
        origination_obj.full_clean()
        origination_obj.save()
        for corpname in xpath(origination, 'e:corpname'):
            name_obj = self._import_name(corpname, CorpName, CorpNamePart)
            origination_obj.corpnames.add(name_obj)
        for famname in xpath(origination, 'e:famname'):
            name_obj = self._import_name(famname, FamName, FamNamePart)
            origination_obj.famnames.add(name_obj)
        for name in xpath(origination, 'e:name'):
            name_obj = self._import_name(name, Name, NamePart)
            origination_obj.names.add(name_obj)
        for persname in xpath(origination, 'e:persname'):
            name_obj = self._import_name(persname, PersName, PersNamePart)
            origination_obj.persnames.add(name_obj)
        origination_obj.full_clean()

    def _import_otheragencycode(self, otheragencycode, ead_obj):
        otheragencycode_obj = OtherAgencyCode(
            maintenanceagency=ead_obj, otheragencycode=otheragencycode.text)
        import_attrs(otheragencycode, OTHERAGENCYCODE_ATTRS,
                     otheragencycode_obj)
        otheragencycode_obj.full_clean()
        otheragencycode_obj.save()

    def _import_otherfindaid(self, otherfindaid, ead_obj):
        otherfindaid_obj = OtherFindAid(
            archdesc=ead_obj, otherfindaid=serialise(otherfindaid))
        import_attrs(otherfindaid, OTHERFINDAID_ATTRS, otherfindaid_obj)
        otherfindaid_obj.full_clean()
        otherfindaid_obj.save()

    def _import_otherrecordid(self, otherrecordid, ead_obj):
        otherrecordid_obj = OtherRecordID(
            control=ead_obj, otherrecordid=otherrecordid.text)
        import_attrs(otherrecordid, OTHERRECORDID_ATTRS, otherrecordid_obj)
        otherrecordid_obj.full_clean()
        otherrecordid_obj.save()

    def _import_part(self, part, name_obj, part_model, position):
        part_obj = part_model(
            name=name_obj, part=serialise(part), order=position+1)
        import_attrs(part, PART_ATTRS, part_obj)
        part_obj.full_clean()
        part_obj.save()

    def _import_physdesc(self, physdesc, ead_obj):
        physdesc_obj = PhysDesc(did=ead_obj, physdesc=serialise(physdesc))
        import_attrs(physdesc, PHYSDESC_ATTRS, physdesc_obj)
        physdesc_obj.full_clean()
        physdesc_obj.save()

    def _import_physdescset(self, physdescset, ead_obj):
        physdescset_obj = PhysDescSet(did=ead_obj)
        import_attrs(physdescset, PHYSDESCSET_ATTRS, physdescset_obj)
        physdescset_obj.full_clean()
        physdescset_obj.save()
        for pds in xpath(physdescset, 'e:physdescstructured'):
            self._import_physdescstructured(pds, physdescset_obj)

    def _import_physdescstructured(self, pds, parent_obj):
        if pds.getparent().tag == EAD_NS + 'did':
            pds_model = DIdPhysDescStructured
            physfacet_model = DIdPhysDescStructuredPhysFacet
            dimensions_model = DIdPhysDescStructuredDimensions
        else:
            pds_model = PhysDescSetPhysDescStructured
            physfacet_model = PhysDescSetPhysDescStructuredPhysFacet
            dimensions_model = PhysDescSetPhyDescStructuredDimensions
        pds_obj = pds_model(parent=parent_obj)
        import_attrs(pds, PHYSDESCSTRUCTURED_ATTRS, pds_obj)
        for quantity in xpath(pds, 'e:quantity'):
            self._import_quantity(quantity, pds_obj)
        for unittype in xpath(pds, 'e:unittype'):
            self._import_unittype(unittype, pds_obj)
        for descriptivenote in xpath(pds, 'e:descriptivenote'):
            self._import_descriptivenote(descriptivenote, pds_obj)
        pds_obj.full_clean()
        pds_obj.save()
        for dimensions in xpath(pds, 'e:dimensions'):
            self._import_dimensions(dimensions, pds_obj, dimensions_model)
        for physfacet in xpath(pds, 'e:physfacet'):
            self._import_physfacet(physfacet, pds_obj, physfacet_model)

    def _import_physfacet(self, physfacet, pds_obj, physfacet_model):
        physfacet_obj = physfacet_model(
            physdescstructured=pds_obj, physfacet=serialise(physfacet))
        import_attrs(physfacet, PHYSFACET_ATTRS, physfacet_obj)
        physfacet_obj.full_clean()
        physfacet_obj.save()

    def _import_physloc(self, physloc, ead_obj):
        physloc_obj = PhysLoc(did=ead_obj, physloc=serialise(physloc))
        import_attrs(physloc, PHYSLOC_ATTRS, physloc_obj)
        physloc_obj.full_clean()
        physloc_obj.save()
        return physloc_obj

    def _import_physloc_parents(self, physloc, physloc_obj, ead_obj):
        for idref in physloc.get('parent', '').split():
            parent_obj = PhysLoc.objects.get(did=ead_obj, ead_id=idref)
            physloc_obj.parents.add(parent_obj)

    def _import_phystech(self, phystech, ead_obj):
        phystech_obj = PhysTech(archdesc=ead_obj, phystech=serialise(phystech))
        import_attrs(phystech, PHYSTECH_ATTRS, phystech_obj)
        phystech_obj.full_clean()
        phystech_obj.save()

    def _import_prefercite(self, prefercite, ead_obj):
        prefercite_obj = PreferCite(
            archdesc=ead_obj, prefercite=serialise(prefercite))
        import_attrs(prefercite, PREFERCITE_ATTRS, prefercite_obj)
        prefercite_obj.full_clean()
        prefercite_obj.save()

    def _import_processinfo(self, processinfo, ead_obj):
        processinfo_obj = ProcessInfo(
            archdesc=ead_obj, processinfo=serialise(processinfo))
        import_attrs(processinfo, PROCESSINFO_ATTRS, processinfo_obj)
        processinfo_obj.full_clean()
        processinfo_obj.save()

    def _import_publicationstatus(self, publicationstatus, ead_obj):
        import_attrs(publicationstatus, PUBLICATIONSTATUS_ATTRS, ead_obj,
                     'publicationstatus_')
        if publicationstatus.text:
            ead_obj.publicationstatus = publicationstatus.text

    def _import_publicationstmt(self, publicationstmt, ead_obj):
        import_attrs(publicationstmt, PUBLICATIONSTMT_ATTRS, ead_obj,
                     'publicationstmt_')
        ead_obj.publicationstmt = serialise(publicationstmt)

    def _import_quantity(self, quantity, physdescstructured_obj):
        physdescstructured_obj.quantity = quantity.text
        import_attrs(quantity, QUANTITY_ATTRS, physdescstructured_obj,
                     'quantity_')

    def _import_recordid(self, recordid, ead_obj):
        ead_obj.recordid = recordid.text
        import_attrs(recordid, RECORDID_ATTRS, ead_obj, 'recordid_')

    def _import_relatedmaterial(self, rm, ead_obj):
        rm_obj = RelatedMaterial(
            archdesc=ead_obj, relatedmaterial=serialise(rm))
        import_attrs(rm, RELATEDMATERIAL_ATTRS, rm_obj)
        rm_obj.full_clean()
        rm_obj.save()

    def _import_relation(self, relation, ead_obj):
        relation_obj = Relation(relations=ead_obj)
        import_attrs(relation, RELATION_ATTRS, relation_obj)
        relation_obj.save()
        for relationentry in xpath(relation, 'e:relationentry'):
            self._import_relationentry(relationentry, relation_obj)
        for objectxmlwrap in xpath(relation, 'e:objectxmlwrap'):
            self._import_objectxmlwrap(objectxmlwrap, relation_obj)
        for daterange in xpath(relation, './/e:daterange'):
            self._import_daterange(daterange, relation_obj, RelationDateRange)
        for dateset in xpath(relation, 'e:dateset'):
            import_attrs(dateset, DATESET_ATTRS, relation_obj, 'dateset_')
        for datesingle in xpath(relation, './/e:datesingle'):
            self._import_datesingle(
                datesingle, relation_obj, RelationDateSingle)
        for geogname in xpath(relation, 'e:geogname'):
            self._import_geogname(geogname, relation_obj)
        for descriptivenote in xpath(relation, 'e:descriptivenote'):
            self._import_descriptivenote(descriptivenote, relation_obj)
        relation_obj.full_clean()
        relation_obj.save()

    def _import_relations(self, relations, ead_obj):
        import_attrs(relations, RELATIONS_ATTRS, ead_obj, 'relations_')
        for relation in relations:
            self._import_relation(relation, ead_obj)

    def _import_relationentry(self, relationentry, relation_obj):
        relationentry_obj = RelationEntry(relation=relation_obj)
        import_attrs(relationentry, RELATIONENTRY_ATTRS, relationentry_obj)
        relationentry_obj.relationentry = relationentry.text
        relationentry_obj.full_clean()
        relationentry_obj.save()

    def _import_repository(self, repository, ead_obj):
        assembled_name = ''.join(xpath(repository, 'e:*/e:part//text()'))
        try:
            repository_obj = Repository.objects.get(
                assembled_name=assembled_name)
            ead_obj.repositories.add(repository_obj)
            return
        except Repository.DoesNotExist:
            pass
        repository_obj = Repository()
        import_attrs(repository, REPOSITORY_ATTRS, repository_obj)
        repository_obj.full_clean()
        repository_obj.save()
        ead_obj.repositories.add(repository_obj)
        for corpname in xpath(repository, 'e:corpname'):
            name_obj = self._import_name(corpname, CorpName, CorpNamePart)
            repository_obj.corpnames.add(name_obj)
        for famname in xpath(repository, 'e:famname'):
            name_obj = self._import_name(famname, FamName, FamNamePart)
            repository_obj.famnames.add(name_obj)
        for name in xpath(repository, 'e:name'):
            name_obj = self._import_name(name, Name, NamePart)
            repository_obj.names.add(name_obj)
        for persname in xpath(repository, 'e:persname'):
            name_obj = self._import_name(persname, PersName, PersNamePart)
            repository_obj.persnames.add(name_obj)
        for address in xpath(repository, 'e:address'):
            self._import_address(address, repository_obj)
        repository_obj.full_clean()
        repository_obj.save()  # To set the assembled_name from the names.

    def _import_representation(self, representation, ead_obj):
        representation_obj = Representation(control=ead_obj)
        import_attrs(representation, REPRESENTATION_ATTRS, representation_obj)
        if representation.text:
            representation_obj.representation = representation.text
        representation_obj.full_clean()
        representation_obj.save()

    def _import_rightsdeclaration(self, rightsdeclaration, ead_obj):
        rd_obj = RightsDeclaration(control=ead_obj)
        import_attrs(rightsdeclaration, RIGHTSDECLARATION_ATTRS, rd_obj)
        for abbr in xpath(rightsdeclaration, 'e:abbr'):
            self._import_abbr(abbr, rd_obj)
        for citation in xpath(rightsdeclaration, 'e:citation'):
            self._import_citation(citation, rd_obj)
        for descriptivenote in xpath(rightsdeclaration, 'e:descriptivenote'):
            self._import_descriptivenote(descriptivenote, rd_obj)
        rd_obj.full_clean()
        rd_obj.save()

    def _import_scopecontent(self, scopecontent, ead_obj):
        scopecontent_obj = ScopeContent(
            archdesc=ead_obj, scopecontent=serialise(scopecontent))
        import_attrs(scopecontent, SCOPECONTENT_ATTRS, scopecontent_obj)
        scopecontent_obj.full_clean()
        scopecontent_obj.save()

    def _import_script(self, script, languageset_obj):
        # script within languagedeclaration is handled within
        # _import_languagedeclaration.
        script_obj = LanguageSetScript(languageset=languageset_obj)
        import_attrs(script, SCRIPT_ATTRS, script_obj)
        scriptcode = script.get('scriptcode')
        if scriptcode:
            script_obj.scriptcode = search_term('iso15924', scriptcode)
        script_obj.script_el = script.text or ''
        script_obj.full_clean()
        script_obj.save()

    def _import_separatedmaterial(self, separatedmaterial, ead_obj):
        separatedmaterial_obj = SeparatedMaterial(
            archdesc=ead_obj, separatedmaterial=serialise(separatedmaterial))
        import_attrs(
            separatedmaterial, SEPARATEDMATERIAL_ATTRS, separatedmaterial_obj)
        separatedmaterial_obj.full_clean()
        separatedmaterial_obj.save()

    def _import_seriesstmt(self, seriesstmt, ead_obj):
        import_attrs(seriesstmt, SERIESSTMT_ATTRS, ead_obj, 'seriesstmt_')
        ead_obj.seriesstmt = serialise(seriesstmt)

    def _import_source(self, source, ead_obj):
        source_obj = Source(sources=ead_obj)
        import_attrs(source, SOURCE_ATTRS, source_obj)
        source_obj.save()
        for sourceentry in xpath(source, 'e:sourceentry'):
            self._import_sourceentry(sourceentry, source_obj)
        for objectxmlwrap in xpath(source, 'e:objectxmlwrap'):
            self._import_objectxmlwrap(objectxmlwrap, source_obj)
        for descriptivenote in xpath(source, 'e:descriptivenote'):
            self._import_descriptivenote(descriptivenote, source_obj)
        source_obj.full_clean()
        source_obj.save()

    def _import_sourceentry(self, sourceentry, source_obj):
        sourceentry_obj = SourceEntry(
            source=source_obj, sourceentry=sourceentry.text)
        import_attrs(sourceentry, SOURCEENTRY_ATTRS, sourceentry_obj)
        sourceentry_obj.full_clean()
        sourceentry_obj.save()

    def _import_sources(self, sources, ead_obj):
        import_attrs(sources, SOURCES_ATTRS, ead_obj, 'sources_')
        for source in sources:
            self._import_source(source, ead_obj)

    def _import_sponsor(self, sponsor, ead_obj):
        sponsor_obj = Sponsor(titlestmt=ead_obj, sponsor=serialise(sponsor))
        import_attrs(sponsor, SPONSOR_ATTRS, sponsor_obj)
        sponsor_obj.full_clean()
        sponsor_obj.save()

    def _import_subtitle(self, subtitle, ead_obj):
        subtitle_obj = Subtitle(
            titlestmt=ead_obj, subtitle=serialise(subtitle))
        import_attrs(subtitle, SUBTITLE_ATTRS, subtitle_obj)
        subtitle_obj.full_clean()
        subtitle_obj.save()

    def _import_term(self, term, localcontrol_obj):
        import_attrs(term, TERM_ATTRS, localcontrol_obj, 'term_')
        localcontrol_obj.term = term.text

    def _import_titleproper(self, titleproper, ead_obj):
        # Use only for titleproper within titlestmt; within
        # seriesstmt, no new model object is created.
        titleproper_obj = TitleProper(
            titlestmt=ead_obj, titleproper=serialise(titleproper))
        import_attrs(titleproper, TITLEPROPER_ATTRS, titleproper_obj)
        titleproper_obj.full_clean()
        titleproper_obj.save()

    def _import_titlestmt(self, titlestmt, ead_obj):
        import_attrs(titlestmt, TITLESTMT_ATTRS, ead_obj, 'titlestmt_')
        for titleproper in xpath(titlestmt, 'e:titleproper'):
            self._import_titleproper(titleproper, ead_obj)
        for subtitle in xpath(titlestmt, 'e:subtitle'):
            self._import_subtitle(subtitle, ead_obj)
        for author in xpath(titlestmt, 'e:author'):
            self._import_author(author, ead_obj)
        for sponsor in xpath(titlestmt, 'e:sponsor'):
            self._import_sponsor(sponsor, ead_obj)

    def _import_unitdate(self, unitdate, ead_obj):
        unitdate_obj = UnitDate(did=ead_obj, unitdate=serialise(unitdate))
        import_attrs(unitdate, UNITDATE_ATTRS, unitdate_obj)
        unitdate_obj.full_clean()
        unitdate_obj.save()

    def _import_unitdatestructured(self, uds, ead_obj):
        uds_obj = UnitDateStructured(did=ead_obj)
        import_attrs(uds, UNITDATESTRUCTURED_ATTRS, uds_obj)
        for dateset in xpath(uds, 'e:dateset'):
            import_attrs(dateset, DATESET_ATTRS, uds_obj, 'dateset_')
        uds_obj.full_clean()
        uds_obj.save()
        for daterange in xpath(uds, './/e:daterange'):
            self._import_daterange(
                daterange, uds_obj, UnitDateStructuredDateRange)
        for datesingle in xpath(uds, './/e:datesingle'):
            self._import_datesingle(
                datesingle, uds_obj, UnitDateStructuredDateSingle)

    def _import_unitid(self, unitid, ead_obj):
        unitid_obj = UnitId(did=ead_obj, unitid=serialise(unitid))
        import_attrs(unitid, UNITID_ATTRS, unitid_obj)
        unitid_obj.full_clean()
        unitid_obj.save()

    def _import_unittitle(self, unittitle, ead_obj):
        unittitle_obj = UnitTitle(did=ead_obj, unittitle=serialise(unittitle))
        import_attrs(unittitle, UNITTITLE_ATTRS, unittitle_obj)
        unittitle_obj.full_clean()
        unittitle_obj.save()

    def _import_unittype(self, unittype, physdescstructured_obj):
        physdescstructured_obj.unittype = unittype.text
        import_attrs(unittype, UNITTYPE_ATTRS, physdescstructured_obj,
                     'unittype_')

    def _import_userestrict(self, userestrict, ead_obj):
        userestrict_obj = UseRestrict(
            archdesc=ead_obj, userestrict=serialise(userestrict))
        import_attrs(userestrict, USERESTRICT_ATTRS, userestrict_obj)
        userestrict_obj.full_clean()
        userestrict_obj.save()
