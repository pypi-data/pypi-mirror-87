from lxml import etree

from .constants import (
    ABBR_ATTRS, ABSTRACT_ATTRS, ACCESSRESTRICT_ATTRS, ACCRUALS_ATTRS,
    ACQINFO_ATTRS, ADDRESS_ATTRS, ADDRESSLINE_ATTRS, AGENCYCODE_ATTRS,
    AGENCYNAME_ATTRS, AGENT_ATTRS, AGENTTYPE_ATTRS, ALTFORMAVAIL_ATTRS,
    APPRAISAL_ATTRS, ARCHDESC_ATTRS, ARRANGEMENT_ATTRS, AUTHOR_ATTRS,
    BIBLIOGRAPHY_ATTRS, BIOGHIST_ATTRS, CITATION_ATTRS, CONTAINER_ATTRS,
    CONTROL_ATTRS, CONTROLACCESS_ATTRS, CONTROLNOTE_ATTRS,
    CONVENTIONDECLARATION_ATTRS, CUSTODHIST_ATTRS, DAO_ATTRS, DAOSET_ATTRS,
    DATERANGE_ATTRS, DATESET_ATTRS, DATESINGLE_ATTRS, DESCRIPTIVENOTE_ATTRS,
    DID_ATTRS, DIDNOTE_ATTRS, DIMENSIONS_ATTRS, EAD_ATTRS, EAD_NAMESPACE,
    EAD_NS as EAD, EDITIONSTMT_ATTRS, EVENTDATETIME_ATTRS,
    EVENTDESCRIPTION_ATTRS, EVENTTYPE_ATTRS, FILEDESC_ATTRS, FILEPLAN_ATTRS,
    FROMTODATE_ATTRS, GEOGNAME_ATTRS, HEAD_ATTRS, INDEX_ATTRS,
    LANGMATERIAL_ATTRS, LANGUAGE_ATTRS, LANGUAGEDECLARATION_ATTRS,
    LANGUAGESET_ATTRS, LEGALSTATUS_ATTRS, LOCALCONTROL_ATTRS,
    LOCALTYPEDECLARATION_ATTRS, MAINTENANCEAGENCY_ATTRS,
    MAINTENANCEEVENT_ATTRS, MAINTENANCEHISTORY_ATTRS, MAINTENANCESTATUS_ATTRS,
    MATERIALSPEC_ATTRS, NAME_ATTRS, NOTESTMT_ATTRS, OBJECTXMLWRAP_ATTRS,
    ODD_ATTRS, ORIGINALSLOC_ATTRS, ORIGINATION_ATTRS, OTHERAGENCYCODE_ATTRS,
    OTHERFINDAID_ATTRS, PART_ATTRS, PHYSDESC_ATTRS, PHYSDESCSET_ATTRS,
    PHYSDESCSTRUCTURED_ATTRS, PHYSFACET_ATTRS, PHYSLOC_ATTRS, PHYSTECH_ATTRS,
    PREFERCITE_ATTRS, PROCESSINFO_ATTRS, PUBLICATIONSTATUS_ATTRS,
    PUBLICATIONSTMT_ATTRS, OTHERRECORDID_ATTRS, QUANTITY_ATTRS, RECORDID_ATTRS,
    RELATEDMATERIAL_ATTRS, RELATION_ATTRS, RELATIONENTRY_ATTRS,
    RELATIONS_ATTRS, REPOSITORY_ATTRS, REPRESENTATION_ATTRS,
    RIGHTSDECLARATION_ATTRS, SCOPECONTENT_ATTRS, SCRIPT_ATTRS,
    SEPARATEDMATERIAL_ATTRS, SERIESSTMT_ATTRS, SOURCE_ATTRS, SOURCEENTRY_ATTRS,
    SOURCES_ATTRS, SPONSOR_ATTRS, SUBTITLE_ATTRS, TERM_ATTRS,
    TITLEPROPER_ATTRS, TITLESTMT_ATTRS, UNITDATE_ATTRS,
    UNITDATESTRUCTURED_ATTRS, UNITID_ATTRS, UNITTITLE_ATTRS, UNITTYPE_ATTRS,
    USERESTRICT_ATTRS)


NS_MAP = {None: EAD_NAMESPACE}


def append_xml(parent, xml):
    if xml:
        root = etree.fromstring('<wrapper>{}</wrapper>'.format(xml))
        parent.text = root.text
        for child in root:
            parent.append(child)


def serialise_attrs(obj, attrs, element, prefix=''):
    for attr in attrs:
        if attr == 'id':
            attr = 'ead_id'
        value = getattr(obj, prefix + attr)
        if value is not None and value != '':
            if isinstance(value, list):
                value = value[0]
            if attr == 'ead_id':
                attr = 'id'
            elif attr in ('lang', 'script'):
                value = value.termid
            elif attr in ('approximate', 'parallel'):
                # BooleanFields.
                value = str(value).lower()
            element.set(attr, str(value))


class EADSerialiser:

    def serialise(self, ead_obj):
        ead = self.to_xml(ead_obj)
        return etree.tostring(ead, encoding='unicode', pretty_print=True)

    def to_xml(self, ead_obj):
        ead = etree.Element(EAD + 'ead', nsmap=NS_MAP)
        serialise_attrs(ead_obj, EAD_ATTRS, ead)
        self._serialise_control(ead_obj, ead)
        self._serialise_archdesc(ead_obj, ead)
        return ead

    def _serialise_abbr(self, parent_obj, parent):
        if not parent_obj.abbr:
            return
        abbr = etree.SubElement(parent, EAD + 'abbr')
        serialise_attrs(parent_obj, ABBR_ATTRS, abbr, 'abbr_')
        abbr.text = parent_obj.abbr

    def _serialise_abstract(self, abstract_obj, did):
        abstract = etree.SubElement(did, EAD + 'abstract')
        serialise_attrs(abstract_obj, ABSTRACT_ATTRS, abstract)
        append_xml(abstract, abstract_obj.abstract)

    def _serialise_accessrestrict(self, accessrestrict_obj, archdesc):
        accessrestrict = etree.SubElement(archdesc, EAD + 'accessrestrict')
        serialise_attrs(
            accessrestrict_obj, ACCESSRESTRICT_ATTRS, accessrestrict)
        append_xml(accessrestrict, accessrestrict_obj.accessrestrict)

    def _serialise_accruals(self, accruals_obj, archdesc):
        accruals = etree.SubElement(archdesc, EAD + 'accruals')
        serialise_attrs(accruals_obj, ACCRUALS_ATTRS, accruals)
        append_xml(accruals, accruals_obj.accruals)

    def _serialise_acqinfo(self, acqinfo_obj, archdesc):
        acqinfo = etree.SubElement(archdesc, EAD + 'acqinfo')
        serialise_attrs(acqinfo_obj, ACQINFO_ATTRS, acqinfo)
        append_xml(acqinfo, acqinfo_obj.acqinfo)

    def _serialise_addressline(self, addressline_obj, address):
        addressline = etree.SubElement(address, EAD + 'addressline')
        serialise_attrs(addressline_obj, ADDRESSLINE_ATTRS, addressline)
        append_xml(addressline, addressline_obj.addressline)

    def _serialise_agencycode(self, ead_obj, maintenanceagency):
        if ead_obj.agencycode:
            agencycode = etree.SubElement(
                maintenanceagency, EAD + 'agencycode')
            serialise_attrs(
                ead_obj, AGENCYCODE_ATTRS, agencycode, 'agencycode_')
            agencycode.text = ead_obj.agencycode

    def _serialise_agencyname(self, agencyname_obj, maintenanceagency):
        agencyname = etree.SubElement(maintenanceagency, EAD + 'agencyname')
        serialise_attrs(agencyname_obj, AGENCYNAME_ATTRS, agencyname)
        agencyname.text = agencyname_obj.agencyname

    def _serialise_agent(self, maintenanceevent_obj, maintenanceevent):
        agent = etree.SubElement(maintenanceevent, EAD + 'agent')
        serialise_attrs(maintenanceevent_obj, AGENT_ATTRS, agent, 'agent_')
        agent.text = maintenanceevent_obj.agent

    def _serialise_agenttype(self, maintenanceevent_obj, maintenanceevent):
        agenttype = etree.SubElement(maintenanceevent, EAD + 'agenttype')
        serialise_attrs(maintenanceevent_obj, AGENTTYPE_ATTRS, agenttype,
                        'agenttype_')
        agenttype.text = maintenanceevent_obj.agenttype

    def _serialise_altformavail(self, altformavail_obj, archdesc):
        altformavail = etree.SubElement(archdesc, EAD + 'altformavail')
        serialise_attrs(altformavail_obj, ALTFORMAVAIL_ATTRS, altformavail)
        append_xml(altformavail, altformavail_obj.altformavail)

    def _serialise_appraisal(self, appraisal_obj, archdesc):
        appraisal = etree.SubElement(archdesc, EAD + 'appraisal')
        serialise_attrs(appraisal_obj, APPRAISAL_ATTRS, appraisal)
        append_xml(appraisal, appraisal_obj.appraisal)

    def _serialise_archdesc(self, ead_obj, ead):
        archdesc = etree.SubElement(ead, EAD + 'archdesc')
        serialise_attrs(ead_obj, ARCHDESC_ATTRS, archdesc, 'archdesc_')
        self._serialise_did(ead_obj, archdesc)
        for accessrestrict_obj in ead_obj.accessrestrict_set.all():
            self._serialise_accessrestrict(accessrestrict_obj, archdesc)
        for accruals_obj in ead_obj.accruals_set.all():
            self._serialise_accruals(accruals_obj, archdesc)
        for acqinfo_obj in ead_obj.acqinfo_set.all():
            self._serialise_acqinfo(acqinfo_obj, archdesc)
        for altformavail_obj in ead_obj.altformavail_set.all():
            self._serialise_altformavail(altformavail_obj, archdesc)
        for appraisal_obj in ead_obj.appraisal_set.all():
            self._serialise_appraisal(appraisal_obj, archdesc)
        for arrangement_obj in ead_obj.arrangement_set.all():
            self._serialise_arrangement(arrangement_obj, archdesc)
        for bibliography_obj in ead_obj.bibliography_set.all():
            self._serialise_bibliography(bibliography_obj, archdesc)
        for bioghist_obj in ead_obj.bioghist_set.all():
            self._serialise_bioghist(bioghist_obj, archdesc)
        for controlaccess_obj in ead_obj.controlaccess_set.all():
            self._serialise_controlaccess(controlaccess_obj, archdesc)
        for custodhist_obj in ead_obj.custodhist_set.all():
            self._serialise_custodhist(custodhist_obj, archdesc)
        for fileplan_obj in ead_obj.fileplan_set.all():
            self._serialise_fileplan(fileplan_obj, archdesc)
        for index_obj in ead_obj.index_set.all():
            self._serialise_index(index_obj, archdesc)
        for legalstatus_obj in ead_obj.legalstatus_set.all():
            self._serialise_legalstatus(legalstatus_obj, archdesc)
        for odd_obj in ead_obj.odd_set.all():
            self._serialise_odd(odd_obj, archdesc)
        for originalsloc_obj in ead_obj.originalsloc_set.all():
            self._serialise_originalsloc(originalsloc_obj, archdesc)
        for otherfindaid_obj in ead_obj.otherfindaid_set.all():
            self._serialise_otherfindaid(otherfindaid_obj, archdesc)
        for phystech_obj in ead_obj.phystech_set.all():
            self._serialise_phystech(phystech_obj, archdesc)
        for prefercite_obj in ead_obj.prefercite_set.all():
            self._serialise_prefercite(prefercite_obj, archdesc)
        for processinfo_obj in ead_obj.processinfo_set.all():
            self._serialise_processinfo(processinfo_obj, archdesc)
        for relatedmaterial_obj in ead_obj.relatedmaterial_set.all():
            self._serialise_relatedmaterial(relatedmaterial_obj, archdesc)
        self._serialise_relations(ead_obj, archdesc)
        for scopecontent_obj in ead_obj.scopecontent_set.all():
            self._serialise_scopecontent(scopecontent_obj, archdesc)
        for separatedmaterial_obj in ead_obj.separatedmaterial_set.all():
            self._serialise_separatedmaterial(separatedmaterial_obj, archdesc)
        for userestrict_obj in ead_obj.userestrict_set.all():
            self._serialise_userestrict(userestrict_obj, archdesc)

    def _serialise_arrangement(self, arrangement_obj, archdesc):
        arrangement = etree.SubElement(archdesc, EAD + 'arrangement')
        serialise_attrs(arrangement_obj, ARRANGEMENT_ATTRS, arrangement)
        append_xml(arrangement, arrangement_obj.arrangement)

    def _serialise_author(self, author_obj, titlestmt):
        author = etree.SubElement(titlestmt, EAD + 'author')
        serialise_attrs(author_obj, AUTHOR_ATTRS, author)
        append_xml(author, author_obj.author)

    def _serialise_bibliography(self, bibliography_obj, archdesc):
        bibliography = etree.SubElement(archdesc, EAD + 'bibliography')
        serialise_attrs(bibliography_obj, BIBLIOGRAPHY_ATTRS, bibliography)
        append_xml(bibliography, bibliography_obj.bibliography)

    def _serialise_bioghist(self, bioghist_obj, archdesc):
        bioghist = etree.SubElement(archdesc, EAD + 'bioghist')
        serialise_attrs(bioghist_obj, BIOGHIST_ATTRS, bioghist)
        append_xml(bioghist, bioghist_obj.bioghist)

    def _serialise_citation(self, parent_obj, parent):
        citation = etree.SubElement(parent, EAD + 'citation')
        serialise_attrs(parent_obj, CITATION_ATTRS, citation, 'citation_')
        append_xml(citation, parent_obj.citation)

    def _serialise_container(self, container_obj, did):
        container = etree.SubElement(did, EAD + 'container')
        serialise_attrs(container_obj, CONTAINER_ATTRS, container)
        parents = [parent.ead_id for parent in container_obj.parents.all()]
        if parents:
            container.set('parent', ' '.join(parents))
        append_xml(container, container_obj.container)

    def _serialise_control(self, ead_obj, ead):
        control = etree.SubElement(ead, EAD + 'control')
        serialise_attrs(ead_obj, CONTROL_ATTRS, control, 'control_')
        self._serialise_recordid(ead_obj, control)
        for otherrecordid_obj in ead_obj.otherrecordid_set.all():
            self._serialise_otherrecordid(otherrecordid_obj, control)
        for representation_obj in ead_obj.representation_set.all():
            self._serialise_representation(representation_obj, control)
        self._serialise_filedesc(ead_obj, control)
        self._serialise_maintenancestatus(ead_obj, control)
        self._serialise_publicationstatus(ead_obj, control)
        self._serialise_maintenanceagency(ead_obj, control)
        for ld_obj in ead_obj.languagedeclarations.all():
            self._serialise_languagedeclaration(ld_obj, control)
        for cd_obj in ead_obj.conventiondeclaration_set.all():
            self._serialise_conventiondeclaration(cd_obj, control)
        for rd_obj in ead_obj.rightsdeclaration_set.all():
            self._serialise_rightsdeclaration(rd_obj, control)
        for ltd_obj in ead_obj.localtypedeclaration_set.all():
            self._serialise_localtypedeclaration(ltd_obj, control)
        for localcontrol_obj in ead_obj.localcontrol_set.all():
            self._serialise_localcontrol(localcontrol_obj, control)
        self._serialise_maintenancehistory(ead_obj, control)
        self._serialise_sources(ead_obj, control)

    def _serialise_controlaccess(self, controlaccess_obj, archdesc):
        controlaccess = etree.SubElement(archdesc, EAD + 'controlaccess')
        serialise_attrs(controlaccess_obj, CONTROLACCESS_ATTRS, controlaccess)
        append_xml(controlaccess, controlaccess_obj.controlaccess)

    def _serialise_controlnote(self, controlnote_obj, notestmt):
        controlnote = etree.SubElement(notestmt, EAD + 'controlnote')
        serialise_attrs(controlnote_obj, CONTROLNOTE_ATTRS, controlnote)
        append_xml(controlnote, controlnote_obj.controlnote)

    def _serialise_conventiondeclaration(self, conventiondeclaration_obj,
                                         control):
        conventiondeclaration = etree.SubElement(
            control, EAD + 'conventiondeclaration')
        serialise_attrs(conventiondeclaration_obj, CONVENTIONDECLARATION_ATTRS,
                        conventiondeclaration)
        self._serialise_abbr(conventiondeclaration_obj, conventiondeclaration)
        self._serialise_citation(
            conventiondeclaration_obj, conventiondeclaration)
        self._serialise_descriptivenote(
            conventiondeclaration_obj, conventiondeclaration)

    def _serialise_custodhist(self, custodhist_obj, archdesc):
        custodhist = etree.SubElement(archdesc, EAD + 'custodhist')
        serialise_attrs(custodhist_obj, CUSTODHIST_ATTRS, custodhist)
        append_xml(custodhist, custodhist_obj.custodhist)

    def _serialise_dao(self, dao_obj, parent):
        dao = etree.SubElement(parent, EAD + 'dao')
        serialise_attrs(dao_obj, DAO_ATTRS, dao)
        self._serialise_descriptivenote(dao_obj, dao)

    def _serialise_daoset(self, daoset_obj, did):
        daoset = etree.SubElement(did, EAD + 'daoset')
        serialise_attrs(daoset_obj, DAOSET_ATTRS, daoset)
        for dao_obj in daoset_obj.dao_set.all():
            self._serialise_dao(dao_obj, daoset)
        self._serialise_descriptivenote(daoset_obj, daoset)

    def _serialise_daterange(self, daterange_obj, parent, prefix=''):
        daterange = etree.SubElement(parent, EAD + 'daterange')
        serialise_attrs(daterange_obj, DATERANGE_ATTRS, daterange, prefix)
        if daterange_obj.fromdate or daterange_obj.fromdate_standarddate:
            self._serialise_fromtodate(daterange_obj, daterange, 'fromdate')
        if daterange_obj.todate or daterange_obj.todate_standarddate:
            self._serialise_fromtodate(daterange_obj, daterange, 'todate')

    def _serialise_dateset(self, obj, parent, daterange_objs, datesingle_objs):
        dateset = etree.SubElement(parent, EAD + 'dateset')
        serialise_attrs(obj, DATESET_ATTRS, dateset, 'dateset_')
        for daterange_obj in daterange_objs:
            self._serialise_daterange(daterange_obj, dateset)
        for datesingle_obj in datesingle_objs:
            self._serialise_datesingle(datesingle_obj, dateset)

    def _serialise_datesingle(self, datesingle_obj, parent, prefix=''):
        datesingle = etree.SubElement(parent, EAD + 'datesingle')
        serialise_attrs(datesingle_obj, DATESINGLE_ATTRS, datesingle, prefix)
        append_xml(datesingle, datesingle_obj.datesingle)

    def _serialise_descriptivenote(self, obj, parent, prefix=''):
        content = getattr(obj, prefix + 'descriptivenote')
        if not content:
            return
        descriptivenote = etree.SubElement(parent, EAD + 'descriptivenote')
        serialise_attrs(obj, DESCRIPTIVENOTE_ATTRS, descriptivenote,
                        prefix + 'descriptivenote_')
        append_xml(descriptivenote, content)

    def _serialise_did(self, ead_obj, archdesc):
        did = etree.SubElement(archdesc, EAD + 'did')
        serialise_attrs(ead_obj, DID_ATTRS, did, 'did_')
        self._serialise_head(ead_obj, did, 'did_')
        for abstract_obj in ead_obj.abstract_set.all():
            self._serialise_abstract(abstract_obj, did)
        for container_obj in ead_obj.container_set.all():
            self._serialise_container(container_obj, did)
        for dao_obj in ead_obj.dao_set.all():
            self._serialise_dao(dao_obj, did)
        for daoset_obj in ead_obj.daoset_set.all():
            self._serialise_daoset(daoset_obj, did)
        for didnote_obj in ead_obj.didnote_set.all():
            self._serialise_didnote(didnote_obj, did)
        for langmaterial_obj in ead_obj.langmaterial_set.all():
            self._serialise_langmaterial(langmaterial_obj, did)
        for materialspec_obj in ead_obj.materialspec_set.all():
            self._serialise_materialspec(materialspec_obj, did)
        for origination_obj in ead_obj.origination_set.all():
            self._serialise_origination(origination_obj, did)
        for physdesc_obj in ead_obj.physdesc_set.all():
            self._serialise_physdesc(physdesc_obj, did)
        for physdescset_obj in ead_obj.physdescset_set.all():
            self._serialise_physdescset(physdescset_obj, did)
        for physdescstructured_obj in ead_obj.physdescstructured_set.all():
            self._serialise_physdescstructured(physdescstructured_obj, did)
        for physloc_obj in ead_obj.physloc_set.all():
            self._serialise_physloc(physloc_obj, did)
        for repository_obj in ead_obj.repositories.all():
            self._serialise_repository(repository_obj, did)
        for unitdate_obj in ead_obj.unitdate_set.all():
            self._serialise_unitdate(unitdate_obj, did)
        for unitdatestructured_obj in ead_obj.unitdatestructured_set.all():
            self._serialise_unitdatestructured(unitdatestructured_obj, did)
        for unitid_obj in ead_obj.unitid_set.all():
            self._serialise_unitid(unitid_obj, did)
        for unittitle_obj in ead_obj.unittitle_set.all():
            self._serialise_unittitle(unittitle_obj, did)

    def _serialise_didnote(self, didnote_obj, did):
        didnote = etree.SubElement(did, EAD + 'didnote')
        serialise_attrs(didnote_obj, DIDNOTE_ATTRS, didnote)
        append_xml(didnote, didnote_obj.didnote)

    def _serialise_dimensions(self, dimensions_obj, pds):
        dimensions = etree.SubElement(pds, EAD + 'dimensions')
        serialise_attrs(dimensions_obj, DIMENSIONS_ATTRS, dimensions)
        append_xml(dimensions, dimensions_obj.dimensions)

    def _serialise_editionstmt(self, ead_obj, filedesc):
        if not ead_obj.editionstmt:
            return
        editionstmt = etree.SubElement(filedesc, EAD + 'editionstmt')
        serialise_attrs(ead_obj, EDITIONSTMT_ATTRS, editionstmt,
                        'editionstmt_')
        append_xml(editionstmt, ead_obj.editionstmt)

    def _serialise_eventdatetime(self, maintenanceevent_obj, maintenanceevent):
        eventdatetime = etree.SubElement(
            maintenanceevent, EAD + 'eventdatetime')
        serialise_attrs(maintenanceevent_obj, EVENTDATETIME_ATTRS,
                        eventdatetime, 'eventdatetime_')
        eventdatetime.text = maintenanceevent_obj.eventdatetime

    def _serialise_eventdescription(self, ed_obj, maintenanceevent):
        eventdescription = etree.SubElement(
            maintenanceevent, EAD + 'eventdescription')
        serialise_attrs(ed_obj, EVENTDESCRIPTION_ATTRS, eventdescription)
        eventdescription.text = ed_obj.eventdescription

    def _serialise_eventtype(self, maintenanceevent_obj, maintenanceevent):
        eventtype = etree.SubElement(maintenanceevent, EAD + 'eventtype')
        serialise_attrs(maintenanceevent_obj, EVENTTYPE_ATTRS, eventtype,
                        'eventtype_')
        eventtype.text = maintenanceevent_obj.eventtype

    def _serialise_filedesc(self, ead_obj, control):
        filedesc = etree.SubElement(control, EAD + 'filedesc')
        serialise_attrs(ead_obj, FILEDESC_ATTRS, filedesc, 'filedesc_')
        self._serialise_titlestmt(ead_obj, filedesc)
        self._serialise_editionstmt(ead_obj, filedesc)
        self._serialise_publicationstmt(ead_obj, filedesc)
        self._serialise_seriesstmt(ead_obj, filedesc)
        self._serialise_notestmt(ead_obj, filedesc)

    def _serialise_fileplan(self, fileplan_obj, archdesc):
        fileplan = etree.SubElement(archdesc, EAD + 'fileplan')
        serialise_attrs(fileplan_obj, FILEPLAN_ATTRS, fileplan)
        append_xml(fileplan, fileplan_obj.fileplan)

    def _serialise_fromtodate(self, daterange_obj, daterange, element_name):
        date = etree.SubElement(daterange, EAD + element_name)
        # Use the individually stored attribute values for the
        # fromdate/todate elements, in place of those on the
        # serialised string.
        serialise_attrs(
            daterange_obj, FROMTODATE_ATTRS, date, element_name + '_')
        append_xml(date, getattr(daterange_obj, element_name))

    def _serialise_geogname(self, relation_obj, relation):
        if not relation_obj.geogname:
            return
        geogname = etree.SubElement(relation, EAD + 'geogname')
        serialise_attrs(relation_obj, GEOGNAME_ATTRS, geogname, 'geogname_')
        append_xml(geogname, relation_obj.geogname)

    def _serialise_head(self, obj, parent, prefix=''):
        content = getattr(obj, prefix + 'head')
        if not content:
            return
        head = etree.SubElement(parent, EAD + 'head')
        serialise_attrs(obj, HEAD_ATTRS, head, prefix + 'head_')
        append_xml(head, content)

    def _serialise_index(self, index_obj, archdesc):
        index = etree.SubElement(archdesc, EAD + 'index')
        serialise_attrs(index_obj, INDEX_ATTRS, index)
        append_xml(index, index_obj.index)

    def _serialise_langmaterial(self, langmaterial_obj, did):
        langmaterial = etree.SubElement(did, EAD + 'langmaterial')
        serialise_attrs(langmaterial_obj, LANGMATERIAL_ATTRS, langmaterial)
        for language_obj in langmaterial_obj.language_set.all():
            self._serialise_language(language_obj, langmaterial)
        for languageset_obj in langmaterial_obj.languageset_set.all():
            self._serialise_languageset(languageset_obj, langmaterial)
        self._serialise_descriptivenote(langmaterial_obj, langmaterial)

    def _serialise_language(self, obj, parent, prefix=''):
        langcode = getattr(obj, prefix + 'langcode')
        if not obj.language and not langcode:
            return
        language = etree.SubElement(parent, EAD + 'language')
        serialise_attrs(obj, LANGUAGE_ATTRS, language, prefix)
        if langcode:
            language.set('langcode', langcode.termid)
        language.text = obj.language

    def _serialise_languagedeclaration(self, ld_obj, control):
        ld = etree.SubElement(control, EAD + 'languagedeclaration')
        serialise_attrs(ld_obj, LANGUAGEDECLARATION_ATTRS, ld)
        self._serialise_language(ld_obj, ld, 'language_')
        self._serialise_script(ld_obj, ld, 'script_el_')
        self._serialise_descriptivenote(ld_obj, ld)

    def _serialise_languageset(self, languageset_obj, langmaterial):
        languageset = etree.SubElement(langmaterial, EAD + 'languageset')
        serialise_attrs(languageset_obj, LANGUAGESET_ATTRS, languageset)
        for language_obj in languageset_obj.language_set.all():
            self._serialise_language(language_obj, languageset)
        for script_obj in languageset_obj.script_set.all():
            self._serialise_script(script_obj, languageset)
        self._serialise_descriptivenote(languageset_obj, languageset)

    def _serialise_legalstatus(self, legalstatus_obj, archdesc):
        legalstatus = etree.SubElement(archdesc, EAD + 'legalstatus')
        serialise_attrs(legalstatus_obj, LEGALSTATUS_ATTRS, legalstatus)
        append_xml(legalstatus, legalstatus_obj.legalstatus)

    def _serialise_localcontrol(self, localcontrol_obj, control):
        localcontrol = etree.SubElement(control, EAD + 'localcontrol')
        serialise_attrs(localcontrol_obj, LOCALCONTROL_ATTRS, localcontrol)
        self._serialise_term(localcontrol_obj, localcontrol)
        if localcontrol_obj.fromdate or localcontrol_obj.todate or \
           localcontrol_obj.fromdate_standarddate or \
           localcontrol_obj.todate_standarddate:
            self._serialise_daterange(
                localcontrol_obj, localcontrol, 'daterange_')
        if localcontrol_obj.datesingle or \
           localcontrol_obj.datesingle_standarddate:
            self._serialise_datesingle(
                localcontrol_obj, localcontrol, 'datesingle_')

    def _serialise_localtypedeclaration(self, ltd_obj, control):
        ltd = etree.SubElement(control, EAD + 'localtypedeclaration')
        serialise_attrs(ltd_obj, LOCALTYPEDECLARATION_ATTRS, ltd)
        self._serialise_abbr(ltd_obj, ltd)
        self._serialise_citation(ltd_obj, ltd)
        self._serialise_descriptivenote(ltd_obj, ltd)

    def _serialise_maintenanceagency(self, ead_obj, control):
        maintenanceagency = etree.SubElement(
            control, EAD + 'maintenanceagency')
        serialise_attrs(ead_obj, MAINTENANCEAGENCY_ATTRS, maintenanceagency,
                        'maintenanceagency_')
        self._serialise_agencycode(ead_obj, maintenanceagency)
        for otheragencycode_obj in ead_obj.otheragencycode_set.all():
            self._serialise_otheragencycode(
                otheragencycode_obj, maintenanceagency)
        for agencyname_obj in ead_obj.agencyname_set.all():
            self._serialise_agencyname(agencyname_obj, maintenanceagency)
        self._serialise_descriptivenote(
            ead_obj, maintenanceagency, 'maintenanceagency_')

    def _serialise_maintenanceevent(self, maintenanceevent_obj,
                                    maintenancehistory):
        maintenanceevent = etree.SubElement(
            maintenancehistory, EAD + 'maintenanceevent')
        serialise_attrs(maintenanceevent_obj, MAINTENANCEEVENT_ATTRS,
                        maintenanceevent)
        self._serialise_eventtype(maintenanceevent_obj, maintenanceevent)
        self._serialise_eventdatetime(maintenanceevent_obj, maintenanceevent)
        self._serialise_agenttype(maintenanceevent_obj, maintenanceevent)
        self._serialise_agent(maintenanceevent_obj, maintenanceevent)
        for ed_obj in maintenanceevent_obj.eventdescription_set.all():
            self._serialise_eventdescription(ed_obj, maintenanceevent)

    def _serialise_maintenancehistory(self, ead_obj, control):
        maintenancehistory = etree.SubElement(
            control, EAD + 'maintenancehistory')
        serialise_attrs(ead_obj, MAINTENANCEHISTORY_ATTRS, maintenancehistory,
                        'maintenancehistory_')
        for maintenanceevent_obj in ead_obj.maintenanceevent_set.all():
            self._serialise_maintenanceevent(
                maintenanceevent_obj, maintenancehistory)

    def _serialise_maintenancestatus(self, ead_obj, control):
        maintenancestatus = etree.SubElement(
            control, EAD + 'maintenancestatus')
        serialise_attrs(ead_obj, MAINTENANCESTATUS_ATTRS, maintenancestatus,
                        'maintenancestatus_')
        if ead_obj.maintenancestatus:
            maintenancestatus.text = ead_obj.maintenancestatus

    def _serialise_materialspec(self, materialspec_obj, did):
        materialspec = etree.SubElement(did, EAD + 'materialspec')
        serialise_attrs(materialspec_obj, MATERIALSPEC_ATTRS, materialspec)
        append_xml(materialspec, materialspec_obj.materialspec)

    def _serialise_name(self, name_obj, parent, element_name):
        name = etree.SubElement(parent, EAD + element_name)
        serialise_attrs(name_obj, NAME_ATTRS, name)
        for part_obj in name_obj.part_set.all():
            self._serialise_part(part_obj, name)

    def _serialise_notestmt(self, ead_obj, filedesc):
        controlnote_objs = ead_obj.controlnote_set.all()
        if controlnote_objs:
            notestmt = etree.SubElement(filedesc, EAD + 'notestmt')
            serialise_attrs(ead_obj, NOTESTMT_ATTRS, notestmt, 'notestmt_')
            for controlnote_obj in controlnote_objs:
                self._serialise_controlnote(controlnote_obj, notestmt)

    def _serialise_objectxmlwrap(self, obj, parent):
        if not obj.objectxmlwrap:
            return
        objectxmlwrap = etree.SubElement(parent, EAD + 'objectxmlwrap')
        serialise_attrs(obj, OBJECTXMLWRAP_ATTRS, objectxmlwrap,
                        'objectxmlwrap_')
        append_xml(objectxmlwrap, obj.objectxmlwrap)

    def _serialise_odd(self, odd_obj, archdesc):
        odd = etree.SubElement(archdesc, EAD + 'odd')
        serialise_attrs(odd_obj, ODD_ATTRS, odd)
        append_xml(odd, odd_obj.odd)

    def _serialise_originalsloc(self, originalsloc_obj, archdesc):
        originalsloc = etree.SubElement(archdesc, EAD + 'originalsloc')
        serialise_attrs(originalsloc_obj, ORIGINALSLOC_ATTRS, originalsloc)
        append_xml(originalsloc, originalsloc_obj.originalsloc)

    def _serialise_origination(self, origination_obj, did):
        origination = etree.SubElement(did, EAD + 'origination')
        serialise_attrs(origination_obj, ORIGINATION_ATTRS, origination)
        for corpname_obj in origination_obj.corpnames.all():
            self._serialise_name(corpname_obj, origination, 'corpname')
        for famname_obj in origination_obj.famnames.all():
            self._serialise_name(famname_obj, origination, 'famname')
        for name_obj in origination_obj.names.all():
            self._serialise_name(name_obj, origination, 'name')
        for persname_obj in origination_obj.persnames.all():
            self._serialise_name(persname_obj, origination, 'persname')

    def _serialise_otheragencycode(self, otheragencycode_obj,
                                   maintenanceagency):
        otheragencycode = etree.SubElement(
            maintenanceagency, EAD + 'otheragencycode')
        serialise_attrs(otheragencycode_obj, OTHERAGENCYCODE_ATTRS,
                        otheragencycode)
        otheragencycode.text = otheragencycode_obj.otheragencycode

    def _serialise_otherfindaid(self, otherfindaid_obj, archdesc):
        otherfindaid = etree.SubElement(archdesc, EAD + 'otherfindaid')
        serialise_attrs(otherfindaid_obj, OTHERFINDAID_ATTRS, otherfindaid)
        append_xml(otherfindaid, otherfindaid_obj.otherfindaid)

    def _serialise_otherrecordid(self, otherrecordid_obj, control):
        otherrecordid = etree.SubElement(control, EAD + 'otherrecordid')
        serialise_attrs(otherrecordid_obj, OTHERRECORDID_ATTRS, otherrecordid)
        otherrecordid.text = otherrecordid_obj.otherrecordid

    def _serialise_part(self, part_obj, name):
        part = etree.SubElement(name, EAD + 'part')
        serialise_attrs(part_obj, PART_ATTRS, part)
        append_xml(part, part_obj.part)

    def _serialise_physdesc(self, physdesc_obj, did):
        physdesc = etree.SubElement(did, EAD + 'physdesc')
        serialise_attrs(physdesc_obj, PHYSDESC_ATTRS, physdesc)
        append_xml(physdesc, physdesc_obj.physdesc)

    def _serialise_physdescset(self, physdescset_obj, did):
        physdescset = etree.SubElement(did, EAD + 'physdescset')
        serialise_attrs(physdescset_obj, PHYSDESCSET_ATTRS, physdescset)
        for pds_obj in physdescset_obj.physdescstructured_set.all():
            self._serialise_physdescstructured(pds_obj, physdescset)

    def _serialise_physdescstructured(self, physdescstructured_obj, parent):
        pds = etree.SubElement(parent, EAD + 'physdescstructured')
        serialise_attrs(physdescstructured_obj, PHYSDESCSTRUCTURED_ATTRS, pds)
        self._serialise_quantity(physdescstructured_obj, pds)
        self._serialise_unittype(physdescstructured_obj, pds)
        for dimensions_obj in physdescstructured_obj.dimensions_set.all():
            self._serialise_dimensions(dimensions_obj, pds)
        for physfacet_obj in physdescstructured_obj.physfacet_set.all():
            self._serialise_physfacet(physfacet_obj, pds)
        self._serialise_descriptivenote(physdescstructured_obj, pds)

    def _serialise_physfacet(self, physfacet_obj, physdescstructured):
        physfacet = etree.SubElement(physdescstructured, EAD + 'physfacet')
        serialise_attrs(physfacet_obj, PHYSFACET_ATTRS, physfacet)
        append_xml(physfacet, physfacet_obj.physfacet)

    def _serialise_physloc(self, physloc_obj, did):
        physloc = etree.SubElement(did, EAD + 'physloc')
        serialise_attrs(physloc_obj, PHYSLOC_ATTRS, physloc)
        parents = [parent.ead_id for parent in physloc_obj.parents.all()]
        if parents:
            physloc.set('parent', ' '.join(parents))
        append_xml(physloc, physloc_obj.physloc)

    def _serialise_phystech(self, phystech_obj, archdesc):
        phystech = etree.SubElement(archdesc, EAD + 'phystech')
        serialise_attrs(phystech_obj, PHYSTECH_ATTRS, phystech)
        append_xml(phystech, phystech_obj.phystech)

    def _serialise_prefercite(self, prefercite_obj, archdesc):
        prefercite = etree.SubElement(archdesc, EAD + 'prefercite')
        serialise_attrs(prefercite_obj, PREFERCITE_ATTRS, prefercite)
        append_xml(prefercite, prefercite_obj.prefercite)

    def _serialise_processinfo(self, processinfo_obj, archdesc):
        processinfo = etree.SubElement(archdesc, EAD + 'processinfo')
        serialise_attrs(processinfo_obj, PROCESSINFO_ATTRS, processinfo)
        append_xml(processinfo, processinfo_obj.processinfo)

    def _serialise_publicationstatus(self, ead_obj, control):
        status = ead_obj.publicationstatus_value
        if not status:
            return
        publicationstatus = etree.SubElement(
            control, EAD + 'publicationstatus')
        serialise_attrs(ead_obj, PUBLICATIONSTATUS_ATTRS, publicationstatus,
                        'publicationstatus_')
        publicationstatus.text = ead_obj.publicationstatus

    def _serialise_publicationstmt(self, ead_obj, filedesc):
        publicationstmt = etree.SubElement(filedesc, EAD + 'publicationstmt')
        serialise_attrs(ead_obj, PUBLICATIONSTMT_ATTRS, publicationstmt,
                        'publicationstmt_')
        append_xml(publicationstmt, ead_obj.publicationstmt)

    def _serialise_quantity(self, physdescstructured_obj, pds):
        if not physdescstructured_obj.quantity:
            return
        quantity = etree.SubElement(pds, EAD + 'quantity')
        serialise_attrs(
            physdescstructured_obj, QUANTITY_ATTRS, quantity, 'quantity_')
        quantity.text = str(physdescstructured_obj.quantity)

    def _serialise_recordid(self, ead_obj, control):
        recordid = etree.SubElement(control, EAD + 'recordid')
        serialise_attrs(ead_obj, RECORDID_ATTRS, recordid, 'recordid_')
        if ead_obj.recordid:
            recordid.text = ead_obj.recordid

    def _serialise_relatedmaterial(self, relatedmaterial_obj, archdesc):
        relatedmaterial = etree.SubElement(archdesc, EAD + 'relatedmaterial')
        serialise_attrs(
            relatedmaterial_obj, RELATEDMATERIAL_ATTRS, relatedmaterial)
        append_xml(relatedmaterial, relatedmaterial_obj.relatedmaterial)

    def _serialise_relation(self, relation_obj, relations):
        relation = etree.SubElement(relations, EAD + 'relation')
        serialise_attrs(relation_obj, RELATION_ATTRS, relation)
        for relationentry_obj in relation_obj.relationentry_set.all():
            self._serialise_relationentry(relationentry_obj, relation)
        self._serialise_objectxmlwrap(relation_obj, relation)
        daterange_objs = relation_obj.daterange_set.all()
        datesingle_objs = relation_obj.datesingle_set.all()
        if len(daterange_objs) + len(datesingle_objs) > 1:
            self._serialise_dateset(
                relation_obj, relation, daterange_objs, datesingle_objs)
        else:
            for daterange_obj in daterange_objs:
                self._serialise_daterange(daterange_obj, relation)
            for datesingle_obj in datesingle_objs:
                self._serialise_datesingle(datesingle_obj, relation)
        self._serialise_geogname(relation_obj, relation)
        self._serialise_descriptivenote(relation_obj, relation)

    def _serialise_relationentry(self, relationentry_obj, relation):
        relationentry = etree.SubElement(relation, EAD + 'relationentry')
        serialise_attrs(relationentry_obj, RELATIONENTRY_ATTRS, relationentry)
        relationentry.text = relationentry_obj.relationentry

    def _serialise_relations(self, ead_obj, archdesc):
        relation_objs = ead_obj.relation_set.all()
        if not relation_objs:
            return
        relations = etree.SubElement(archdesc, EAD + 'relations')
        serialise_attrs(ead_obj, RELATIONS_ATTRS, relations, 'relations_')
        for relation_obj in relation_objs:
            self._serialise_relation(relation_obj, relations)

    def _serialise_repository(self, repository_obj, did):
        repository = etree.SubElement(did, EAD + 'repository')
        serialise_attrs(repository_obj, REPOSITORY_ATTRS, repository)
        for corpname_obj in repository_obj.corpnames.all():
            self._serialise_name(corpname_obj, repository, 'corpname')
        for famname_obj in repository_obj.famnames.all():
            self._serialise_name(famname_obj, repository, 'famname')
        for name_obj in repository_obj.names.all():
            self._serialise_name(name_obj, repository, 'name')
        for persname_obj in repository_obj.persnames.all():
            self._serialise_name(persname_obj, repository, 'persname')
        addressline_objs = repository_obj.addressline_set.all()
        if addressline_objs:
            address = etree.SubElement(repository, EAD + 'address')
            serialise_attrs(repository_obj, ADDRESS_ATTRS, address, 'address_')
            for addressline_obj in addressline_objs:
                self._serialise_addressline(addressline_obj, address)

    def _serialise_representation(self, representation_obj, control):
        representation = etree.SubElement(control, EAD + 'representation')
        serialise_attrs(representation_obj, REPRESENTATION_ATTRS,
                        representation)
        representation.text = representation_obj.representation

    def _serialise_rightsdeclaration(self, rightsdeclaration_obj, control):
        rightsdeclaration = etree.SubElement(
            control, EAD + 'rightsdeclaration')
        serialise_attrs(rightsdeclaration_obj, RIGHTSDECLARATION_ATTRS,
                        rightsdeclaration)
        self._serialise_abbr(rightsdeclaration_obj, rightsdeclaration)
        self._serialise_citation(rightsdeclaration_obj, rightsdeclaration)
        self._serialise_descriptivenote(
            rightsdeclaration_obj, rightsdeclaration)

    def _serialise_scopecontent(self, scopecontent_obj, parent):
        scopecontent = etree.SubElement(parent, EAD + 'scopecontent')
        serialise_attrs(scopecontent_obj, SCOPECONTENT_ATTRS, scopecontent)
        append_xml(scopecontent, scopecontent_obj.scopecontent)

    def _serialise_script(self, obj, parent, prefix=''):
        scriptcode = getattr(obj, prefix + 'scriptcode')
        if not obj.script_el and not scriptcode:
            return
        script = etree.SubElement(parent, EAD + 'script')
        serialise_attrs(obj, SCRIPT_ATTRS, script, prefix)
        if scriptcode:
            script.set('scriptcode', scriptcode.termid)
        script.text = obj.script_el

    def _serialise_separatedmaterial(self, sm_obj, archdesc):
        sm = etree.SubElement(archdesc, EAD + 'separatedmaterial')
        serialise_attrs(sm_obj, SEPARATEDMATERIAL_ATTRS, sm)
        append_xml(sm, sm_obj.separatedmaterial)

    def _serialise_seriesstmt(self, ead_obj, filedesc):
        if not ead_obj.seriesstmt:
            return
        seriesstmt = etree.SubElement(filedesc, EAD + 'seriesstmt')
        serialise_attrs(ead_obj, SERIESSTMT_ATTRS, seriesstmt, 'seriesstmt_')
        append_xml(seriesstmt, ead_obj.seriesstmt)

    def _serialise_source(self, source_obj, sources):
        source = etree.SubElement(sources, EAD + 'source')
        serialise_attrs(source_obj, SOURCE_ATTRS, source)
        for sourceentry_obj in source_obj.sourceentry_set.all():
            self._serialise_sourceentry(sourceentry_obj, source)
        self._serialise_objectxmlwrap(source_obj, source)
        self._serialise_descriptivenote(source_obj, source)

    def _serialise_sourceentry(self, sourceentry_obj, source):
        sourceentry = etree.SubElement(source, EAD + 'sourceentry')
        serialise_attrs(sourceentry_obj, SOURCEENTRY_ATTRS, sourceentry)
        sourceentry.text = sourceentry_obj.sourceentry

    def _serialise_sources(self, ead_obj, control):
        source_objs = ead_obj.source_set.all()
        if not source_objs:
            return
        sources = etree.SubElement(control, EAD + 'sources')
        serialise_attrs(ead_obj, SOURCES_ATTRS, sources, 'sources_')
        for source_obj in source_objs:
            self._serialise_source(source_obj, sources)

    def _serialise_sponsor(self, sponsor_obj, titlestmt):
        sponsor = etree.SubElement(titlestmt, EAD + 'sponsor')
        serialise_attrs(sponsor_obj, SPONSOR_ATTRS, sponsor)
        append_xml(sponsor, sponsor_obj.sponsor)

    def _serialise_subtitle(self, subtitle_obj, titlestmt):
        subtitle = etree.SubElement(titlestmt, EAD + 'subtitle')
        serialise_attrs(subtitle_obj, SUBTITLE_ATTRS, subtitle)
        append_xml(subtitle, subtitle_obj.subtitle)

    def _serialise_term(self, localcontrol_obj, localcontrol):
        if localcontrol_obj.term:
            term = etree.SubElement(localcontrol, EAD + 'term')
            serialise_attrs(localcontrol_obj, TERM_ATTRS, term, 'term_')
            term.text = localcontrol_obj.term

    def _serialise_titleproper(self, titleproper_obj, parent):
        titleproper = etree.SubElement(parent, EAD + 'titleproper')
        serialise_attrs(titleproper_obj, TITLEPROPER_ATTRS, titleproper)
        append_xml(titleproper, titleproper_obj.titleproper)

    def _serialise_titlestmt(self, ead_obj, filedesc):
        titlestmt = etree.SubElement(filedesc, EAD + 'titlestmt')
        serialise_attrs(ead_obj, TITLESTMT_ATTRS, titlestmt, 'titlestmt_')
        for titleproper_obj in ead_obj.titleproper_set.all():
            self._serialise_titleproper(titleproper_obj, titlestmt)
        for subtitle_obj in ead_obj.subtitle_set.all():
            self._serialise_subtitle(subtitle_obj, titlestmt)
        for author_obj in ead_obj.author_set.all():
            self._serialise_author(author_obj, titlestmt)
        for sponsor_obj in ead_obj.sponsor_set.all():
            self._serialise_sponsor(sponsor_obj, titlestmt)

    def _serialise_unitdate(self, unitdate_obj, did):
        unitdate = etree.SubElement(did, EAD + 'unitdate')
        serialise_attrs(unitdate_obj, UNITDATE_ATTRS, unitdate)
        append_xml(unitdate, unitdate_obj.unitdate)

    def _serialise_unitdatestructured(self, unitdatestructured_obj, did):
        unitdatestructured = etree.SubElement(did, EAD + 'unitdatestructured')
        serialise_attrs(unitdatestructured_obj, UNITDATESTRUCTURED_ATTRS,
                        unitdatestructured)
        daterange_objs = unitdatestructured_obj.daterange_set.all()
        datesingle_objs = unitdatestructured_obj.datesingle_set.all()
        if len(daterange_objs) + len(datesingle_objs) > 1:
            self._serialise_dateset(
                unitdatestructured_obj, unitdatestructured, daterange_objs,
                datesingle_objs)
        else:
            for daterange_obj in daterange_objs:
                self._serialise_daterange(daterange_obj, unitdatestructured)
            for datesingle_obj in datesingle_objs:
                self._serialise_datesingle(datesingle_obj, unitdatestructured)

    def _serialise_unitid(self, unitid_obj, did):
        unitid = etree.SubElement(did, EAD + 'unitid')
        serialise_attrs(unitid_obj, UNITID_ATTRS, unitid)
        append_xml(unitid, unitid_obj.unitid)

    def _serialise_unittitle(self, unittitle_obj, did):
        unittitle = etree.SubElement(did, EAD + 'unittitle')
        serialise_attrs(unittitle_obj, UNITTITLE_ATTRS, unittitle)
        append_xml(unittitle, unittitle_obj.unittitle)

    def _serialise_unittype(self, physdescstructured_obj, pds):
        if not physdescstructured_obj.unittype:
            return
        unittype = etree.SubElement(pds, EAD + 'unittype')
        serialise_attrs(
            physdescstructured_obj, UNITTYPE_ATTRS, unittype, 'unittype_')
        unittype.text = physdescstructured_obj.unittype

    def _serialise_userestrict(self, userestrict_obj, archdesc):
        userestrict = etree.SubElement(archdesc, EAD + 'userestrict')
        serialise_attrs(userestrict_obj, USERESTRICT_ATTRS, userestrict)
        append_xml(userestrict, userestrict_obj.userestrict)
