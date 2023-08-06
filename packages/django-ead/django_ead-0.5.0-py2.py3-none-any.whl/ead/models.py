"""Models representing the Encoded Archival Description (EAD) version
3 specification.

Coverage:

* Does not support the EAD3 dsc element, as it may be deprecated in
  future versions of EAD and its content model is horrific.

* Each of the elements that contain mixed content are handled via a
  TextField that should hold serialised XML of that element. This XML
  should be validated on model save.

* Due to the former point, some elements do not get their own
  fields. Others do for their existence within certain contexts (eg.
  abbr).

* @entityref is not supported.


Naming conventions:

* ForeignKey fields on models that represent an element are named for
  the element that contains that element in the XML
  representation. Thus Source has a sources field that is a ForeignKey
  pointing to the EAD model. This preserves the logic of the XML
  representation, rather than privileging the particular
  implementation in Django (which is less aggregated than one model
  per element, for reasons of performance and sanity.

  Exceptions to this are elements that may be children to multiple
  parents: the parts of names (CorpNamePart, FamNamePart, NamePart,
  and PersNamePart), which all use "name" as the fieldname of the
  ForeignKey to the parent name; various date elements, dao, language,
  and physdescstructured, which use "parent".

* Field names use the same name as the XML element and attribute names
  rather than Python style, but may have a prefix to maintain
  uniqueness. This allows relatively simple automatic setting of
  values when importing from EAD XML. This pattern had to be broken
  for the element "script", due to clashes with the (much more
  frequent) attribute "script". All fields relating to the element use
  "script_el". Likewise the attribute "id" had to be renamed to
  "ead_id" so as not to clash with the default primary key field for
  each model.

* related_name hasn't been set for relationship fields, except where
  this adds significant clarity or allows for generic handling.


Extra fields:

* Some models have extra fields that do not correspond to an element
  or attribute. The order field on the name parts captures the
  ordering of elements. In order to allow selecting existing objects
  in order to reuse them, Repository stores a name assembled from its
  component names, and similarly each of CorpName, FamName, Name, and
  PersName stores a name assembled from its component parts.


Model validation:

* Validation of certain fields based on the XML attribute requirements
  (NMTOKEN, etc) is handled.

* XML content model validation is handled partly through the model
  definitions and occasionally with clean methods. The latter are used
  in cases where at least one of a number of options is required, but
  cannot be a full solution where many-to-many relationships are
  involved - an instance needs to exist before it can be associated
  through a ManyToManyField, and so validation will not be run on
  initial creation.

* The content model of certain XML elements is not yet validated, but
  should be handled in future through specific validators that use
  snippets of the EAD3 XSD to perform XML validation.

"""
from copy import deepcopy
from xml.sax.saxutils import escape

from django.core.exceptions import ValidationError
from django.db import models

from lxml import etree

from controlled_vocabulary.models import ControlledTermField

import reversion

from .serialisers import EADSerialiser
from .validators import (
    validate_date_time, validate_id, validate_nmtoken, validate_token)
from . import constants


ACTUATE_NONE = 'none'
ACTUATE_ONLOAD = 'onload'
ACTUATE_ONREQUEST = 'onrequest'
ACTUATE_OTHER = 'other'
ACTUATE_CHOICES = [
    (ACTUATE_NONE, 'None'),
    (ACTUATE_ONLOAD, 'onload'),
    (ACTUATE_ONREQUEST, 'onrequest'),
    (ACTUATE_OTHER, 'Other'),
]

EXTERNAL_AUDIENCE = 'external'
INTERNAL_AUDIENCE = 'internal'
AUDIENCE_CHOICES = [
    (EXTERNAL_AUDIENCE, 'External'),
    (INTERNAL_AUDIENCE, 'Internal'),
]

SHOW_EMBED = 'embed'
SHOW_NEW = 'new'
SHOW_NONE = 'none'
SHOW_OTHER = 'other'
SHOW_REPLACE = 'replace'
SHOW_CHOICES = [
    (SHOW_EMBED, 'Embed'),
    (SHOW_NEW, 'New'),
    (SHOW_NONE, 'None'),
    (SHOW_OTHER, 'Other'),
    (SHOW_REPLACE, 'Replace'),
]


# Given the need to have multiple fields within a single model
# representing the same XML attributes, only associated with different
# elements, define such fields outside a model and use deepcopy to
# include them under custom names within the models.

actuate = models.CharField(blank=True, choices=ACTUATE_CHOICES, max_length=9)
altrender = models.CharField(
    blank=True, max_length=128, validators=[validate_token])
arcrole = models.CharField(blank=True, max_length=512)
audience = models.CharField(
    blank=True, choices=AUDIENCE_CHOICES, max_length=8)
base = models.CharField(blank=True, max_length=128)
countrycode = models.CharField(
    blank=True, max_length=64, validators=[validate_nmtoken])
encodinganalog = models.CharField(
    blank=True, max_length=64, validators=[validate_token])
ead_id = models.CharField(blank=True, max_length=64, validators=[validate_id])
href = models.CharField(
    blank=True, max_length=512, validators=[validate_token])
identifier = models.CharField(
    blank=True, max_length=512, validators=[validate_token])
label = models.CharField(blank=True, max_length=128)
lang = ControlledTermField(
    ['iso639-2'], blank=True, help_text=constants.LANGUAGE_HELP,
    null=True, on_delete=models.PROTECT)
lastdatetimeverified = models.CharField(
    blank=True, max_length=25, validators=[validate_date_time])
linkrole = models.CharField(blank=True, max_length=512)
linktitle = models.CharField(
    blank=True, max_length=512, validators=[validate_token])
localtype = models.CharField(
    blank=True, max_length=512, validators=[validate_token])
normal = models.CharField(
    blank=True, max_length=128, validators=[validate_token])
notafter = models.CharField(
    blank=True, max_length=32, validators=[validate_token])
notbefore = models.CharField(
    blank=True, max_length=32, validators=[validate_token])
relator = models.CharField(
    blank=True, max_length=64, validators=[validate_token])
rules = models.CharField(
    blank=True, max_length=64, validators=[validate_nmtoken])
script = ControlledTermField(
    ['iso15924'], blank=True, null=True, on_delete=models.PROTECT)
show = models.CharField(blank=True, choices=SHOW_CHOICES, max_length=7)
source = models.CharField(
    blank=True, max_length=64, validators=[validate_token])
standarddate = models.CharField(
    blank=True, max_length=32, validators=[validate_token])
transliteration = models.CharField(
    blank=True, max_length=64, validators=[validate_nmtoken])


# Mixins for fields corresponding to EAD3 attributes.

class AccessMixin(models.Model):
    """Corresponds to EAD3 @identifier, @rules, and @source."""
    identifier = deepcopy(identifier)
    rules = deepcopy(rules)
    source = deepcopy(source)

    class Meta:
        abstract = True


class BaseMixin(models.Model):
    """Corresponds to EAD3 @base."""
    base = deepcopy(base)

    class Meta:
        abstract = True


class CommonMixin(models.Model):
    """Corresponds to EAD3 @altrender, @audience, and @id."""
    altrender = deepcopy(altrender)
    audience = deepcopy(audience)
    ead_id = deepcopy(ead_id)

    class Meta:
        abstract = True


class CoverageMixin(models.Model):
    """Corresponds to EAD3 @coverage."""
    COVERAGE_PART = 'part'
    COVERAGE_WHOLE = 'whole'
    COVERAGE_CHOICES = [
        (COVERAGE_PART, 'Part'),
        (COVERAGE_WHOLE, 'Whole'),
    ]
    coverage = models.CharField(
        blank=True, choices=COVERAGE_CHOICES, max_length=5)

    class Meta:
        abstract = True


class DateAttrMixin(models.Model):
    """Corresponds to EAD3 @calendar, @certainty, and @era."""
    calendar = models.CharField(blank=True, max_length=64, validators=[
        validate_nmtoken])
    certainty = models.CharField(blank=True, max_length=64, validators=[
        validate_nmtoken])
    era = models.CharField(blank=True, max_length=64, validators=[
        validate_nmtoken])

    class Meta:
        abstract = True


class EncodingAnalogMixin(models.Model):
    """Corresponds to EAD3 @encodinganalog."""
    encodinganalog = deepcopy(encodinganalog)

    class Meta:
        abstract = True


class LabelMixin(models.Model):
    """Corresponds to EAD3 @label."""
    label = deepcopy(label)

    class Meta:
        abstract = True


class LangScriptMixin(models.Model):
    """Corresponds to EAD3 @lang and @script."""
    lang = deepcopy(lang)
    script = deepcopy(script)

    class Meta:
        abstract = True


class LinkMixin(models.Model):
    """Corresponds to EAD3 @actuate, @arcrole, @href, @linkrole,
    @linktitle, @show."""
    actuate = deepcopy(actuate)
    arcrole = deepcopy(arcrole)
    href = deepcopy(href)
    linkrole = deepcopy(linkrole)
    linktitle = deepcopy(linktitle)
    show = deepcopy(show)

    class Meta:
        abstract = True


class LocalTypeMixin(models.Model):
    """Corresponds to EAD3 @localtype."""
    localtype = deepcopy(localtype)

    class Meta:
        abstract = True


class NormalMixin(models.Model):
    """Corresponds to EAD3 @normal."""
    normal = deepcopy(normal)

    class Meta:
        abstract = True


class RelatedEncodingMixin(models.Model):
    """Corresponds to EAD3 @relatedencoding."""
    relatedencoding = models.CharField(
        blank=True, max_length=64, validators=[validate_token])

    class Meta:
        abstract = True


class RelatorMixin(models.Model):
    """Corresponds to EAD3 @relator."""
    relator = deepcopy(relator)

    class Meta:
        abstract = True


class TransliterationMixin(models.Model):
    """Corresponds to EAD3 @transliteration."""
    transliteration = deepcopy(transliteration)

    class Meta:
        abstract = True


class UnitDateAttrMixin(DateAttrMixin):
    """Corresponds to EAD3 @datechar, @unitdatetype (and @calendar,
    @certainty and @era via DateAttrMixin)."""
    UNIT_DATE_TYPE_BULK = 'bulk'
    UNIT_DATE_TYPE_INCLUSIVE = 'inclusive'
    UNIT_DATE_TYPE_CHOICES = [
        (UNIT_DATE_TYPE_BULK, 'Bulk'),
        (UNIT_DATE_TYPE_INCLUSIVE, 'Inclusive'),
    ]
    datechar = models.CharField(
        blank=True, max_length=64, validators=[validate_token])
    unitdatetype = models.CharField(
        blank=True, choices=UNIT_DATE_TYPE_CHOICES, max_length=9)

    class Meta:
        abstract = True


class XPointerMixin(models.Model):
    """Corresponds to EAD3 @xpointer."""
    xpointer = models.CharField(
        blank=True, max_length=512, validators=[validate_token])

    class Meta:
        abstract = True


# Mixins for fields corresponding to EAD3 elements.
#
# Many of these do not inherit from attribute mixins but rather have
# those attributes explicitly added with a model-specific prefix. This
# is to ensure uniqueness when the mixin is used in a model that
# inherits from another mixin that has those attributes.
#
# If the EAD3 element the mixin corresponds to is repeatable,
# attribute mixins may be used; otherwise not.


class AbbrMixin(models.Model):
    """Corresponds to EAD3 abbr."""
    abbr = models.CharField(blank=True, max_length=64)
    abbr_altrender = deepcopy(altrender)
    abbr_audience = deepcopy(audience)
    abbr_expan = models.CharField(blank=True, max_length=512)
    abbr_ead_id = deepcopy(ead_id)
    abbr_lang = deepcopy(lang)
    abbr_script = deepcopy(script)

    class Meta:
        abstract = True


class CitationMixin(models.Model):
    """Corresponds to EAD3 citation."""
    citation = models.TextField()
    citation_actuate = deepcopy(actuate)
    citation_altrender = deepcopy(altrender)
    citation_arcrole = deepcopy(arcrole)
    citation_audience = deepcopy(audience)
    citation_encodinganalog = deepcopy(encodinganalog)
    citation_href = deepcopy(href)
    citation_ead_id = deepcopy(ead_id)
    citation_lang = deepcopy(lang)
    citation_lastdatetimeverified = deepcopy(lastdatetimeverified)
    citation_linkrole = deepcopy(linkrole)
    citation_linktitle = deepcopy(linktitle)
    citation_script = deepcopy(script)
    citation_show = deepcopy(show)

    class Meta:
        abstract = True


class DateMixin(CommonMixin, DateAttrMixin, EncodingAnalogMixin,
                LangScriptMixin, LocalTypeMixin, NormalMixin):
    """Corresponds to EAD3 date.

    The date field must support the following markup (or markup that
    can be converted to): abbr, emph, expan, foreign, lb, ptr,
    ref. These further may have markup children of their own.

    """
    date = models.TextField()

    class Meta:
        abstract = True


class DateRangeMixin(CommonMixin, LangScriptMixin, LocalTypeMixin):
    """Corresponds to EAD3 daterange."""
    # date_range contains from_date and to_date.
    fromdate_altrender = deepcopy(altrender)
    fromdate_audience = deepcopy(audience)
    fromdate_ead_id = deepcopy(ead_id)
    fromdate_lang = deepcopy(lang)
    fromdate_localtype = deepcopy(localtype)
    fromdate_notafter = deepcopy(notafter)
    fromdate_notbefore = deepcopy(notbefore)
    fromdate_script = deepcopy(script)
    fromdate_standarddate = deepcopy(standarddate)
    fromdate = models.TextField(blank=True)
    todate_altrender = deepcopy(altrender)
    todate_audience = deepcopy(audience)
    todate_ead_id = deepcopy(ead_id)
    todate_lang = deepcopy(lang)
    todate_localtype = deepcopy(localtype)
    todate_notafter = deepcopy(notafter)
    todate_notbefore = deepcopy(notbefore)
    todate_script = deepcopy(script)
    todate_standarddate = deepcopy(standarddate)
    todate = models.TextField(blank=True)

    class Meta:
        abstract = True


class DateSetMixin(models.Model):
    """Corresponds to EAD3 dateset."""
    dateset_altrender = deepcopy(altrender)
    dateset_audience = deepcopy(audience)
    dateset_ead_id = deepcopy(ead_id)
    dateset_lang = deepcopy(lang)
    dateset_localtype = deepcopy(localtype)
    dateset_script = deepcopy(script)

    class Meta:
        abstract = True


class DateSingleMixin(CommonMixin, LangScriptMixin, LocalTypeMixin):
    """Corresponds to EAD3 datesingle."""
    notafter = deepcopy(notafter)
    notbefore = deepcopy(notbefore)
    standarddate = deepcopy(standarddate)
    datesingle = models.TextField(blank=True)

    class Meta:
        abstract = True


class DescriptiveNoteMixin(models.Model):
    """Corresponds to EAD3 descriptivenote."""
    descriptivenote = models.TextField(blank=True)
    descriptivenote_altrender = deepcopy(altrender)
    descriptivenote_audience = deepcopy(audience)
    descriptivenote_encodinganalog = deepcopy(encodinganalog)
    descriptivenote_ead_id = deepcopy(ead_id)
    descriptivenote_lang = deepcopy(lang)
    descriptivenote_script = deepcopy(script)

    class Meta:
        abstract = True


class DimensionsMixin(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                      LocalTypeMixin):
    """Corresponds to EAD3 dimensions."""
    unit = models.CharField(
        blank=True, max_length=64, validators=[validate_token])
    dimensions = models.TextField()

    class Meta:
        abstract = True


class LanguageMixin(models.Model):
    """Corresponds to the text content of EAD3 language."""
    language = models.CharField(max_length=32)


class NameMixin(models.Model):
    """Provides an extra field and save method for name models that stores
    a name assembled from its parts."""
    assembled_name = models.TextField(blank=True)

    def clean(self):
        if self.pk is None:
            return
        if self.part_set.count() == 0:
            raise ValidationError('A {} must have at least one part.'.format(
                self._meta.object_name))

    def save(self, *args, **kwargs):
        self.assembled_name = ''.join(
            self.part_set.values_list('plain_name', flat=True))
        super().save(*args, **kwargs)

    def __str__(self):
        if self.normal:
            name = self.normal
        else:
            name = self.assembled_name
        return name

    class Meta:
        abstract = True


class ObjectXMLWrapMixin(models.Model):
    """Corresponds to EAD3 objectxmlwrap."""
    objectxmlwrap_altrender = deepcopy(altrender)
    objectxmlwrap_audience = deepcopy(audience)
    objectxmlwrap_ead_id = deepcopy(ead_id)
    objectxmlwrap_lang = deepcopy(lang)
    objectxmlwrap_script = deepcopy(script)
    objectxmlwrap = models.TextField(blank=True)

    class Meta:
        abstract = True


class PartMixin(AccessMixin, CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                LocalTypeMixin):
    """Corresponds to EAD3 part.

    The part field must support the following markup (or markup that
    can be converted to): abbr, date, emph, expan, foreign, lb, ptr,
    ref. These further may have markup children of their own.

    The plain_name field holds the text value of part.

    """
    part = models.TextField()
    order = models.PositiveSmallIntegerField()
    plain_name = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        part_xml = etree.fromstring('<wrapper>{}</wrapper>'.format(
            escape(self.part)))
        self.plain_name = ''.join(part_xml.xpath('.//text()'))
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class PhysDescStructuredMixin(CommonMixin, CoverageMixin, EncodingAnalogMixin,
                              LabelMixin, LangScriptMixin,
                              DescriptiveNoteMixin):
    """Corresponds to EAD3 physdescstructured."""
    STRUCTURED_TYPE_CARRIER = 'carrier'
    STRUCTURED_TYPE_MATERIAL = 'materialtype'
    STRUCTURED_TYPE_OTHER = 'otherphysdescstructuredtype'
    STRUCTURED_TYPE_SPACE = 'spaceoccupied'
    PHYS_DESC_STRUCTURED_TYPE_CHOICES = [
        (STRUCTURED_TYPE_CARRIER, 'Carrier'),
        (STRUCTURED_TYPE_MATERIAL, 'Material type'),
        (STRUCTURED_TYPE_OTHER, 'Other'),
        (STRUCTURED_TYPE_SPACE, 'Space occupied'),
    ]
    physdescstructuredtype = models.CharField(
        choices=PHYS_DESC_STRUCTURED_TYPE_CHOICES, max_length=27)
    otherphysdescstructuredtype = models.CharField(
        blank=True, max_length=64, validators=[validate_token])
    quantity_altrender = deepcopy(altrender)
    quantity_approximate = models.BooleanField(blank=True, null=True)
    quantity_audience = deepcopy(audience)
    quantity_encodinganalog = deepcopy(encodinganalog)
    quantity_ead_id = deepcopy(ead_id)
    quantity_lang = deepcopy(lang)
    quantity_script = deepcopy(script)
    quantity = models.IntegerField(blank=True, null=True)
    unittype_altrender = deepcopy(altrender)
    unittype_audience = deepcopy(audience)
    unittype_encodinganalog = deepcopy(encodinganalog)
    unittype_ead_id = deepcopy(ead_id)
    unittype_identifier = deepcopy(identifier)
    unittype_lang = deepcopy(lang)
    unittype_rules = deepcopy(rules)
    unittype_script = deepcopy(script)
    unittype_source = deepcopy(source)
    unittype = models.CharField(max_length=64)

    class Meta:
        abstract = True


class PhysFacetMixin(AccessMixin, CommonMixin, EncodingAnalogMixin,
                     LabelMixin, LangScriptMixin, LocalTypeMixin):
    """Correponds to EAD3 physfacet."""
    physfacet = models.TextField()

    class Meta:
        abstract = True


class ScriptMixin(models.Model):
    """Corresponds to text content of EAD3 script."""
    script_el = models.CharField(blank=True, max_length=32)

    class Meta:
        abstract = True


class DAOMixin(CommonMixin, CoverageMixin, EncodingAnalogMixin, LabelMixin,
               LangScriptMixin, LinkMixin, LocalTypeMixin, XPointerMixin,
               DescriptiveNoteMixin):
    """Corresponds to EAD3 dao."""
    DAO_TYPE_BORN_DIGITAL = 'borndigital'
    DAO_TYPE_DERIVED = 'derived'
    DAO_TYPE_UNKNOWN = 'unknown'
    DAO_TYPE_OTHER = 'otherdaotype'
    DAO_TYPE_CHOICES = [
        (DAO_TYPE_BORN_DIGITAL, 'Born digital'),
        (DAO_TYPE_DERIVED, 'Derived'),
        (DAO_TYPE_UNKNOWN, 'Unknown'),
        (DAO_TYPE_OTHER, 'Other'),
    ]
    daotype = models.CharField(choices=DAO_TYPE_CHOICES, max_length=12)
    identifier = deepcopy(identifier)
    otherdaotype = models.CharField(
        blank=True, max_length=64, validators=[validate_token])

    class Meta:
        abstract = True


# Section models, abstract models that are inherited usually by a
# single model and which must not make use of mixins in order to avoid
# inheriting the same field multiple times. Attributes that would
# usually come from mixins are prefixed with the section name to make
# them unique.

class EditionStmtSection(models.Model):
    """Corresponds to EAD3 editionstmt."""
    editionstmt = models.TextField(blank=True)
    editionstmt_altrender = deepcopy(altrender)
    editionstmt_audience = deepcopy(audience)
    editionstmt_encodinganalog = deepcopy(encodinganalog)
    editionstmt_ead_id = deepcopy(ead_id)
    editionstmt_lang = deepcopy(lang)
    editionstmt_script = deepcopy(script)

    class Meta:
        abstract = True


class NotesStmtSection(models.Model):
    """Corresponds to EAD3 notestmt."""
    notestmt_altrender = deepcopy(altrender)
    notestmt_audience = deepcopy(audience)
    notestmt_encodinganalog = deepcopy(encodinganalog)
    notestmt_ead_id = deepcopy(ead_id)
    notestmt_lang = deepcopy(lang)
    notestmt_script = deepcopy(script)

    class Meta:
        abstract = True


class PublicationStmtSection(models.Model):
    """Corresponds to EAD3 publicationstmt."""
    publicationstmt = models.TextField(blank=True)
    publicationstmt_altrender = deepcopy(altrender)
    publicationstmt_audience = deepcopy(audience)
    publicationstmt_encodinganalog = deepcopy(encodinganalog)
    publicationstmt_ead_id = deepcopy(ead_id)
    publicationstmt_lang = deepcopy(lang)
    publicationstmt_script = deepcopy(script)

    class Meta:
        abstract = True


class SeriesStmtSection(models.Model):
    """Corresponds to EAD3 seriesstmt."""
    seriesstmt = models.TextField(blank=True)
    seriesstmt_altrender = deepcopy(altrender)
    seriesstmt_audience = deepcopy(audience)
    seriesstmt_encodinganalog = deepcopy(encodinganalog)
    seriesstmt_ead_id = deepcopy(ead_id)
    seriesstmt_lang = deepcopy(lang)
    seriesstmt_script = deepcopy(script)

    class Meta:
        abstract = True


class TitleStmtSection(models.Model):
    """Corresponds to EAD3 titlestmt."""
    titlestmt_altrender = deepcopy(altrender)
    titlestmt_audience = deepcopy(audience)
    titlestmt_encodinganalog = deepcopy(encodinganalog)
    titlestmt_ead_id = deepcopy(ead_id)
    titlestmt_lang = deepcopy(lang)
    titlestmt_script = deepcopy(script)

    class Meta:
        abstract = True


class FileDescSection(EditionStmtSection, NotesStmtSection,
                      PublicationStmtSection, SeriesStmtSection,
                      TitleStmtSection):
    """Corresponds to EAD3 filedesc."""
    filedesc_altrender = deepcopy(altrender)
    filedesc_audience = deepcopy(audience)
    filedesc_encodinganalog = deepcopy(encodinganalog)
    filedesc_ead_id = deepcopy(ead_id)
    filedesc_lang = deepcopy(lang)
    filedesc_script = deepcopy(script)

    class Meta:
        abstract = True


class MaintenanceSection(models.Model):
    """Corresponds to EAD3 maintenanceagency, maintenancehistory,
    maintenancestatus."""
    MAINTENANCE_STATUS_REVISED = 'revised'
    MAINTENANCE_STATUS_DELETED = 'deleted'
    MAINTENANCE_STATUS_NEW = 'new'
    MAINTENANCE_STATUS_DELETED_SPLIT = 'deletedsplit'
    MAINTENANCE_STATUS_DELETED_MERGED = 'deletedmerged'
    MAINTENANCE_STATUS_DELETED_REPLACED = 'deletedreplaced'
    MAINTENANCE_STATUS_CANCELLED = 'cancelled'
    MAINTENANCE_STATUS_DERIVED = 'derived'
    MAINTENANCE_STATUS_CHOICES = [
        (MAINTENANCE_STATUS_REVISED, 'Revised'),
        (MAINTENANCE_STATUS_DELETED, 'Deleted'),
        (MAINTENANCE_STATUS_NEW, 'New'),
        (MAINTENANCE_STATUS_DELETED_SPLIT, 'Deleted split'),
        (MAINTENANCE_STATUS_DELETED_MERGED, 'Deleted merged'),
        (MAINTENANCE_STATUS_DELETED_REPLACED, 'Deleted replaced'),
        (MAINTENANCE_STATUS_CANCELLED, 'Cancelled'),
        (MAINTENANCE_STATUS_DERIVED, 'Derived'),
    ]
    maintenanceagency_altrender = deepcopy(altrender)
    maintenanceagency_audience = deepcopy(audience)
    maintenanceagency_countrycode = deepcopy(countrycode)
    maintenanceagency_encodinganalog = deepcopy(encodinganalog)
    maintenanceagency_ead_id = deepcopy(ead_id)
    maintenanceagency_lang = deepcopy(lang)
    maintenanceagency_script = deepcopy(script)
    agencycode_altrender = deepcopy(altrender)
    agencycode_audience = deepcopy(audience)
    agencycode_encodinganalog = deepcopy(encodinganalog)
    agencycode_ead_id = deepcopy(ead_id)
    agencycode_lang = deepcopy(lang)
    agencycode_localtype = deepcopy(localtype)
    agencycode_script = deepcopy(script)
    agencycode = models.CharField(blank=True, max_length=32)
    maintenanceagency_descriptivenote = models.TextField(blank=True)
    maintenanceagency_descriptivenote_altrender = deepcopy(altrender)
    maintenanceagency_descriptivenote_audience = deepcopy(audience)
    maintenanceagency_descriptivenote_encodinganalog = deepcopy(encodinganalog)
    maintenanceagency_descriptivenote_ead_id = deepcopy(ead_id)
    maintenanceagency_descriptivenote_lang = deepcopy(lang)
    maintenanceagency_descriptivenote_script = deepcopy(script)

    maintenancehistory_altrender = deepcopy(altrender)
    maintenancehistory_audience = deepcopy(audience)
    maintenancehistory_encodinganalog = deepcopy(encodinganalog)
    maintenancehistory_ead_id = deepcopy(ead_id)
    maintenancehistory_lang = deepcopy(lang)
    maintenancehistory_script = deepcopy(script)

    maintenancestatus_altrender = deepcopy(altrender)
    maintenancestatus_audience = deepcopy(audience)
    maintenancestatus_encodinganalog = deepcopy(encodinganalog)
    maintenancestatus_ead_id = deepcopy(ead_id)
    maintenancestatus_lang = deepcopy(lang)
    maintenancestatus_script = deepcopy(script)
    maintenancestatus_value = models.CharField(
        choices=MAINTENANCE_STATUS_CHOICES, max_length=15)
    maintenancestatus = models.CharField(blank=True, max_length=64)

    class Meta:
        abstract = True


class PublicationStatusSection(models.Model):
    """Corresponds to EAD3 publicationstatus."""
    PUBLICATION_STATUS_INPROCESS = 'inprocess'
    PUBLICATION_STATUS_APPROVED = 'approved'
    PUBLICATION_STATUS_PUBLISHED = 'published'
    PUBLICATION_STATUS_CHOICES = [
        (PUBLICATION_STATUS_INPROCESS, 'In process'),
        (PUBLICATION_STATUS_APPROVED, 'Approved'),
        (PUBLICATION_STATUS_PUBLISHED, 'Published'),
    ]

    publicationstatus_altrender = deepcopy(altrender)
    publicationstatus_audience = deepcopy(audience)
    publicationstatus_encodinganalog = deepcopy(encodinganalog)
    publicationstatus_ead_id = deepcopy(ead_id)
    publicationstatus_lang = deepcopy(lang)
    publicationstatus_script = deepcopy(script)
    publicationstatus_value = models.CharField(
        blank=True, choices=PUBLICATION_STATUS_CHOICES, max_length=9)
    publicationstatus = models.CharField(blank=True, max_length=64)

    class Meta:
        abstract = True


class RecordIdSection(models.Model):
    """Corresponds to EAD3 recordid."""
    recordid_altrender = deepcopy(altrender)
    recordid_audience = deepcopy(audience)
    recordid_encodinganalog = deepcopy(encodinganalog)
    recordid_ead_id = deepcopy(ead_id)
    recordid_lang = deepcopy(lang)
    recordid_script = deepcopy(script)
    recordid_instanceurl = models.CharField(blank=True, max_length=512)
    recordid = models.CharField(max_length=64, unique=True)

    class Meta:
        abstract = True


class SourcesSection(models.Model):
    """Corresponds to EAD3 sources."""
    sources_altrender = deepcopy(altrender)
    sources_audience = deepcopy(audience)
    sources_base = models.CharField(blank=True, max_length=128)
    sources_encodinganalog = deepcopy(encodinganalog)
    sources_ead_id = deepcopy(ead_id)
    sources_lang = deepcopy(lang)
    sources_localtype = deepcopy(localtype)
    sources_script = deepcopy(script)

    class Meta:
        abstract = True


class ControlSection(FileDescSection, MaintenanceSection,
                     PublicationStatusSection, RecordIdSection,
                     SourcesSection):
    ISO_COUNTRY_ENCODING = 'iso3166-1'
    OTHER_COUNTRY_ENCODING = 'othercountryencoding'
    COUNTRY_ENCODING_CHOICES = [
        (ISO_COUNTRY_ENCODING, 'ISO 3166-1'),
        (OTHER_COUNTRY_ENCODING, 'Other Country Encoding'),
    ]
    ISO_DATE_ENCODING = 'iso8601'
    OTHER_DATE_ENCODING = 'otherdateencoding'
    DATE_ENCODING_CHOICES = [
        (ISO_DATE_ENCODING, 'ISO 8601'),
        (OTHER_DATE_ENCODING, 'Other Date Encoding'),
    ]
    ISO_639_1_LANG_ENCODING = 'iso639-1'
    ISO_639_2B_LANG_ENCODING = 'iso639-2b'
    ISO_639_3_LANG_ENCODING = 'iso639-3'
    OTHER_LANG_ENCODING = 'otherlangencoding'
    LANG_ENCODING_CHOICES = [
        (ISO_639_1_LANG_ENCODING, 'ISO 639-1'),
        (ISO_639_2B_LANG_ENCODING, 'ISO 639-2b'),
        (ISO_639_3_LANG_ENCODING, 'ISO 639-3'),
        (OTHER_LANG_ENCODING, 'Other Language Encoding'),
    ]
    ISO_REPOSITORY_ENCODING = 'iso15511'
    OTHER_REPOSITORY_ENCODING = 'otherrepositoryencoding'
    REPOSITORY_ENCODING_CHOICES = [
        (ISO_REPOSITORY_ENCODING, 'ISO 15511'),
        (OTHER_REPOSITORY_ENCODING, 'Other Repository Encoding'),
    ]
    ISO_SCRIPT_ENCODING = 'iso15924'
    OTHER_SCRIPT_ENCODING = 'otherscriptencoding'
    SCRIPT_ENCODING_CHOICES = [
        (ISO_SCRIPT_ENCODING, 'ISO 15924'),
        (OTHER_SCRIPT_ENCODING, 'Other Script Encoding'),
    ]

    control_altrender = deepcopy(altrender)
    control_audience = deepcopy(audience)
    control_base = models.CharField(blank=True, max_length=128)
    control_countryencoding = models.CharField(
        blank=True, choices=COUNTRY_ENCODING_CHOICES, max_length=20)
    control_dateencoding = models.CharField(
        blank=True, choices=DATE_ENCODING_CHOICES, max_length=17)
    control_encodinganalog = deepcopy(encodinganalog)
    control_ead_id = deepcopy(ead_id)
    control_lang = deepcopy(lang)
    control_langencoding = models.CharField(
        blank=True, choices=LANG_ENCODING_CHOICES, max_length=17)
    control_relatedencoding = models.CharField(
        blank=True, max_length=64, validators=[validate_token])
    control_repositoryencoding = models.CharField(
        blank=True, choices=REPOSITORY_ENCODING_CHOICES, max_length=23)
    control_script = deepcopy(script)
    control_scriptencoding = models.CharField(
        blank=True, choices=SCRIPT_ENCODING_CHOICES, max_length=19)

    class Meta:
        abstract = True


class DIdSection(models.Model):
    """Correponds to EAD3 did."""
    did_altrender = deepcopy(altrender)
    did_audience = deepcopy(audience)
    did_encodinganalog = deepcopy(encodinganalog)
    did_ead_id = deepcopy(ead_id)
    did_lang = deepcopy(lang)
    did_script = deepcopy(script)
    did_head = models.TextField(blank=True)
    did_head_althead = models.CharField(blank=True, max_length=64)
    did_head_altrender = deepcopy(altrender)
    did_head_audience = deepcopy(audience)
    did_head_ead_id = deepcopy(ead_id)
    did_head_lang = deepcopy(lang)
    did_head_script = deepcopy(script)

    class Meta:
        abstract = True


class RelationsSection(models.Model):
    """Corresponds to EAD3 relations."""
    relations_altrender = deepcopy(altrender)
    relations_audience = deepcopy(audience)
    relations_base = models.CharField(blank=True, max_length=128)
    relations_encodinganalog = deepcopy(encodinganalog)
    relations_ead_id = deepcopy(ead_id)
    relations_lang = deepcopy(lang)
    relations_localtype = deepcopy(localtype)
    relations_script = deepcopy(script)

    class Meta:
        abstract = True


class ArchDescSection(DIdSection, RelationsSection):
    """Corresponds to EAD3 archdesc."""
    LEVEL_CLASS = 'class'
    LEVEL_COLLECTION = 'collection'
    LEVEL_FILE = 'file'
    LEVEL_FONDS = 'fonds'
    LEVEL_ITEM = 'item'
    LEVEL_OTHER_LEVEL = 'otherlevel'
    LEVEL_RECORD_GROUP = 'recordgrp'
    LEVEL_SERIES = 'series'
    LEVEL_SUB_FONDS = 'subfonds'
    LEVEL_SUB_GROUP = 'subgrp'
    LEVEL_SUB_SERIES = 'subseries'
    LEVEL_CHOICES = [
        (LEVEL_CLASS, 'Class'),
        (LEVEL_COLLECTION, 'Collection'),
        (LEVEL_FILE, 'File'),
        (LEVEL_FONDS, 'Fonds'),
        (LEVEL_ITEM, 'Item'),
        (LEVEL_OTHER_LEVEL, 'Other level'),
        (LEVEL_RECORD_GROUP, 'Record group'),
        (LEVEL_SERIES, 'Series'),
        (LEVEL_SUB_FONDS, 'Sub-fonds'),
        (LEVEL_SUB_GROUP, 'Sub-group'),
        (LEVEL_SUB_SERIES, 'Sub-series'),
    ]
    archdesc_altrender = deepcopy(altrender)
    archdesc_audience = deepcopy(audience)
    archdesc_base = models.CharField(blank=True, max_length=128)
    archdesc_encodinganalog = deepcopy(encodinganalog)
    archdesc_ead_id = deepcopy(ead_id)
    archdesc_lang = deepcopy(lang)
    archdesc_level = models.CharField(choices=LEVEL_CHOICES, max_length=10)
    archdesc_localtype = deepcopy(localtype)
    archdesc_otherlevel = models.CharField(blank=True, max_length=32)
    archdesc_relatedencoding = models.CharField(
        blank=True, max_length=64, validators=[validate_token])
    archdesc_script = deepcopy(script)

    class Meta:
        abstract = True


@reversion.register(follow=[
    'abstract_set', 'accessrestrict_set', 'accruals_set', 'acqinfo_set',
    'agencyname_set', 'altformavail_set', 'appraisal_set', 'arrangement_set',
    'author_set', 'bibliography_set', 'bioghist_set', 'container_set',
    'controlaccess_set', 'controlnote_set', 'conventiondeclaration_set',
    'custodhist_set', 'dao_set', 'daoset_set', 'didnote_set', 'fileplan_set',
    'index_set', 'langmaterial_set', 'legalstatus_set', 'localcontrol_set',
    'localtypedeclaration_set', 'maintenanceevent_set', 'materialspec_set',
    'odd_set', 'originalsloc_set', 'origination_set', 'otheragencycode_set',
    'otherfindaid_set', 'otherrecordid_set', 'physdesc_set', 'physdescset_set',
    'physdescstructured_set', 'physloc_set', 'phystech_set', 'prefercite_set',
    'processinfo_set', 'relatedmaterial_set', 'relation_set',
    'representation_set', 'rightsdeclaration_set', 'scopecontent_set',
    'separatedmaterial_set', 'source_set', 'sponsor_set', 'subtitle_set',
    'titleproper_set', 'unitdate_set', 'unitdatestructured_set', 'unitid_set',
    'unittitle_set', 'userestrict_set'])
class EAD(BaseMixin, CommonMixin, LangScriptMixin, RelatedEncodingMixin,
          ControlSection, ArchDescSection):
    # In order to avoid as many levels of joins as we can without
    # sacrificing adherence to EAD3, sacrifice not repeating
    # ourselves. Non-repeatable elements are kept in the model of
    # their parent. This requires repeating mixin model fields with
    # modified names.
    #
    # In order to provide some degree of organisation, sections are in
    # their own abstract models and inherited.
    #
    # Some fields that properly belong in one of the *Section abstract
    # models are defined here in order to avoid having to specify a
    # cumbersome related_name.
    languagedeclarations = models.ManyToManyField(
        'LanguageDeclaration', blank=True)
    repositories = models.ManyToManyField(
        'Repository', blank=True, help_text=constants.REPOSITORY_HELP)

    def serialise(self):
        """Return this object (and its related objects) serialised as a
        complete EAD3 XML document.

        :rtype: `str`

        """
        serialiser = EADSerialiser()
        return serialiser.serialise(self)

    def __str__(self):
        unittitles = self.unittitle_set.values_list('unittitle', flat=True)
        return ' - '.join(unittitles)

    def to_xml(self):
        """Return this object (and its related objects) as an EAD3 XML
        document.

        :rtype: `lxml.etree._Element

        """
        serialiser = EADSerialiser()
        return serialiser.to_xml(self)


@reversion.register()
class Abstract(CommonMixin, EncodingAnalogMixin, LabelMixin, LangScriptMixin,
               LocalTypeMixin):
    """Corresponds to EAD3 abstract."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)
    abstract = models.TextField()


@reversion.register()
class AccessRestrict(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                     LocalTypeMixin):
    """Corresponds to EAD3 accessrestrict."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    accessrestrict = models.TextField()


@reversion.register()
class Accruals(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
               LocalTypeMixin):
    """Corresponds to EAD3 accruals."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    accruals = models.TextField()


@reversion.register()
class AcqInfo(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
              LocalTypeMixin):
    """Corresponds to EAD3 acqinfo."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    acqinfo = models.TextField()


@reversion.register()
class AgencyName(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                 LocalTypeMixin):
    """Corresponds to EAD3 agencyname."""
    maintenanceagency = models.ForeignKey(EAD, on_delete=models.CASCADE)
    agencyname = models.TextField()


@reversion.register()
class AltFormAvail(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                   LocalTypeMixin):
    """Corresponds to EAD3 altformavail."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    altformavail = models.TextField()


@reversion.register()
class Appraisal(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                LocalTypeMixin):
    """Corresponds to EAD3 appraisal."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    appraisal = models.TextField()


@reversion.register()
class Arrangement(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                  LocalTypeMixin):
    """Corresponds to EAD3 arrangement."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    arrangement = models.TextField()


@reversion.register()
class Author(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
             LocalTypeMixin):
    """Corresponds to EAD3 author."""
    titlestmt = models.ForeignKey(EAD, on_delete=models.CASCADE)
    author = models.TextField()


@reversion.register()
class Bibliography(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                   LocalTypeMixin):
    """Corresponds to EAD3 bibliography."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    bibliography = models.TextField()


@reversion.register()
class BiogHist(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
               LocalTypeMixin):
    """Corresponds to EAD3 bioghist."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    bioghist = models.TextField()


@reversion.register()
class Container(CommonMixin, EncodingAnalogMixin, LabelMixin, LangScriptMixin,
                LocalTypeMixin):
    """Corresponds to EAD3 container."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)
    container = models.TextField()
    containerid = models.CharField(blank=True, max_length=128)
    parents = models.ManyToManyField(
        'self', blank=True, related_name='child_containers', symmetrical=False)


@reversion.register()
class ControlAccess(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                    LocalTypeMixin):
    """Corresponds to EAD3 controlaccess."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    controlaccess = models.TextField()


@reversion.register()
class ControlNote(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                  LocalTypeMixin):
    """Corresponds to EAD3 controlnote.

    The controlnote field must support the following markup (or
    markup that can be converted to): blockquote, chronlist, list, p,
    table. These further may have markup children of their own.

    """
    notestmt = models.ForeignKey(EAD, on_delete=models.CASCADE)
    controlnote = models.TextField()


@reversion.register()
class ConventionDeclaration(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                            LocalTypeMixin, AbbrMixin, CitationMixin,
                            DescriptiveNoteMixin):
    """Corresponds to EAD3 conventiondeclaration."""
    control = models.ForeignKey(EAD, on_delete=models.CASCADE)


@reversion.register(follow=['part_set'])
class CorpName(AccessMixin, CommonMixin, EncodingAnalogMixin, LangScriptMixin,
               LocalTypeMixin, NormalMixin, RelatorMixin, NameMixin):
    """Corresponds to EAD3 corpname."""
    pass


@reversion.register()
class CorpNamePart(PartMixin):
    """Corresponds to EAD3 part as a child of corpname."""
    name = models.ForeignKey(
        CorpName, on_delete=models.CASCADE, related_name='part_set')

    class Meta:
        ordering = ['order']
        unique_together = ['name', 'order']


@reversion.register()
class CustodHist(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                 LocalTypeMixin):
    """Corresponds to EAD3 custodhist."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    custodhist = models.TextField()


@reversion.register()
class DIdDAO(DAOMixin):
    """Corresponds to EAD3 dao as a child of did."""
    parent = models.ForeignKey(
        EAD, on_delete=models.CASCADE, related_name='dao_set')


@reversion.register()
class DIdNote(CommonMixin, EncodingAnalogMixin, LabelMixin, LangScriptMixin,
              LocalTypeMixin):
    """Corresponds to EAD3 didnote."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)
    didnote = models.TextField()


@reversion.register(follow=['dimensions_set', 'physfacet_set'])
class DIdPhysDescStructured(PhysDescStructuredMixin):
    """Corresponds to EAD3 physdescstrutured as a child of did."""
    parent = models.ForeignKey(
        EAD, on_delete=models.CASCADE, related_name='physdescstructured_set')


@reversion.register()
class DIdPhysDescStructuredDimensions(DimensionsMixin):
    """Corresponds to EAD3 dimensions as a grandchild of did."""
    physdescstructured = models.ForeignKey(
        DIdPhysDescStructured, on_delete=models.CASCADE,
        related_name='dimensions_set')


@reversion.register()
class DIdPhysDescStructuredPhysFacet(PhysFacetMixin):
    """Corresponds to EAD3 physfacet as a grandchild of did"""
    physdescstructured = models.ForeignKey(
        DIdPhysDescStructured, on_delete=models.CASCADE,
        related_name='physfacet_set')


@reversion.register(follow=['dao_set'])
class DAOSet(BaseMixin, CommonMixin, CoverageMixin, EncodingAnalogMixin,
             LabelMixin, LangScriptMixin, LocalTypeMixin,
             DescriptiveNoteMixin):
    """Corresponds to EAD3 daoset."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)


@reversion.register()
class DAOSetDAO(DAOMixin):
    """Corresponds to EAD3 dao as a child of daoset."""
    parent = models.ForeignKey(
        DAOSet, on_delete=models.CASCADE, related_name='dao_set')


@reversion.register()
class EventDescription(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                       LocalTypeMixin):
    """Corresponds to EAD3 eventdescription."""
    maintenanceevent = models.ForeignKey(
        'MaintenanceEvent', on_delete=models.CASCADE)
    eventdescription = models.TextField()


@reversion.register(follow=['part_set'])
class FamName(AccessMixin, CommonMixin, EncodingAnalogMixin, LangScriptMixin,
              LocalTypeMixin, NormalMixin, RelatorMixin, NameMixin):
    """Corresponds to EAD3 famname."""
    pass


@reversion.register()
class FamNamePart(PartMixin):
    """Corresponds to EAD3 part as a child of famname."""
    name = models.ForeignKey(
        FamName, on_delete=models.CASCADE, related_name='part_set')

    class Meta:
        ordering = ['order']
        unique_together = ['name', 'order']


@reversion.register()
class FilePlan(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
               LocalTypeMixin):
    """Corresponds to EAD3 fileplan."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    fileplan = models.TextField()


@reversion.register()
class Index(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
            LocalTypeMixin):
    """Corresponds to EAD3 index."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    index = models.TextField()


@reversion.register(follow=['language_set', 'languageset_set'])
class LangMaterial(CommonMixin, EncodingAnalogMixin, LabelMixin,
                   LangScriptMixin, DescriptiveNoteMixin):
    """Corresponds to EAD3 langmaterial."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)


@reversion.register()
class LangMaterialLanguage(CommonMixin, EncodingAnalogMixin, LabelMixin,
                           LangScriptMixin, LanguageMixin):
    """Corresponds to EAD3 language as a child of langmaterial."""
    parent = models.ForeignKey(
        LangMaterial, on_delete=models.CASCADE, related_name='language_set')
    langcode = deepcopy(lang)


@reversion.register()
class LanguageDeclaration(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                          DescriptiveNoteMixin, LanguageMixin, ScriptMixin):
    """Corresponds to EAD3 languagedeclaration.

    Exists in a ManyToMany relationship with EAD (Control), since it
    seems likely that within a project most records will use the same
    language(s) and script(s).

    """
    language_altrender = deepcopy(altrender)
    language_audience = deepcopy(audience)
    language_encodinganalog = deepcopy(encodinganalog)
    language_ead_id = deepcopy(ead_id)
    language_label = deepcopy(label)
    language_lang = deepcopy(lang)
    language_langcode = deepcopy(lang)
    language_script = deepcopy(script)
    script_el_altrender = deepcopy(altrender)
    script_el_audience = deepcopy(audience)
    script_el_scriptcode = deepcopy(script)
    script_el_encodinganalog = deepcopy(encodinganalog)
    script_el_ead_id = deepcopy(ead_id)
    script_el_label = deepcopy(label)
    script_el_lang = deepcopy(lang)
    script_el_script = deepcopy(script)


@reversion.register(follow=['language_set', 'script_set'])
class LanguageSet(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                  DescriptiveNoteMixin):
    """Corresponds to EAD3 languageset."""
    langmaterial = models.ForeignKey(LangMaterial, on_delete=models.CASCADE)


@reversion.register()
class LanguageSetLanguage(CommonMixin, EncodingAnalogMixin, LabelMixin,
                          LangScriptMixin, LanguageMixin):
    """Corresponds to EAD3 language as a child of languageset."""
    parent = models.ForeignKey(
        LanguageSet, on_delete=models.CASCADE, related_name='language_set')
    langcode = deepcopy(lang)


@reversion.register()
class LanguageSetScript(CommonMixin, EncodingAnalogMixin, LabelMixin,
                        LangScriptMixin, ScriptMixin):
    """Corresponds to EAD3 script as a child of languageset."""
    languageset = models.ForeignKey(
        LanguageSet, on_delete=models.CASCADE, related_name='script_set')
    scriptcode = deepcopy(script)


@reversion.register()
class LegalStatus(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                  LocalTypeMixin):
    """Corresponds to EAD3 legalstatus."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    legalstatus = models.TextField()


@reversion.register()
class LocalControl(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                   LocalTypeMixin):
    """Corresponds to EAD3 localcontrol."""
    control = models.ForeignKey(EAD, on_delete=models.CASCADE)
    term = models.CharField(blank=True, max_length=64)
    term_altrender = deepcopy(altrender)
    term_audience = deepcopy(audience)
    term_encodinganalog = deepcopy(encodinganalog)
    term_ead_id = deepcopy(ead_id)
    term_identifier = deepcopy(identifier)
    term_lang = deepcopy(lang)
    term_lastdatetimeverified = deepcopy(lastdatetimeverified)
    term_rules = deepcopy(rules)
    term_script = deepcopy(script)
    term_source = deepcopy(source)
    term_transliteration = deepcopy(transliteration)
    daterange_altrender = deepcopy(altrender)
    daterange_audience = deepcopy(audience)
    daterange_ead_id = deepcopy(ead_id)
    daterange_lang = deepcopy(lang)
    daterange_localtype = deepcopy(localtype)
    daterange_script = deepcopy(script)
    fromdate = models.TextField(blank=True)
    fromdate_altrender = deepcopy(altrender)
    fromdate_audience = deepcopy(audience)
    fromdate_ead_id = deepcopy(ead_id)
    fromdate_lang = deepcopy(lang)
    fromdate_localtype = deepcopy(localtype)
    fromdate_notafter = deepcopy(notafter)
    fromdate_notbefore = deepcopy(notbefore)
    fromdate_script = deepcopy(script)
    fromdate_standarddate = deepcopy(standarddate)
    todate = models.TextField(blank=True)
    todate_altrender = deepcopy(altrender)
    todate_audience = deepcopy(audience)
    todate_ead_id = deepcopy(ead_id)
    todate_lang = deepcopy(lang)
    todate_localtype = deepcopy(localtype)
    todate_notafter = deepcopy(notafter)
    todate_notbefore = deepcopy(notbefore)
    todate_script = deepcopy(script)
    todate_standarddate = deepcopy(standarddate)
    datesingle = models.TextField(blank=True)
    datesingle_altrender = deepcopy(altrender)
    datesingle_audience = deepcopy(audience)
    datesingle_ead_id = deepcopy(ead_id)
    datesingle_lang = deepcopy(lang)
    datesingle_localtype = deepcopy(localtype)
    datesingle_notafter = deepcopy(notafter)
    datesingle_notbefore = deepcopy(notbefore)
    datesingle_script = deepcopy(script)
    datesingle_standarddate = deepcopy(standarddate)


@reversion.register()
class LocalTypeDeclaration(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                           AbbrMixin, CitationMixin, DescriptiveNoteMixin):
    """Corresponds to EAD3 localtypedeclaration."""
    control = models.ForeignKey(EAD, on_delete=models.CASCADE)


@reversion.register(follow=['eventdescription_set'])
class MaintenanceEvent(CommonMixin, EncodingAnalogMixin, LangScriptMixin):
    """Corresponds to EAD3 maintenanceevent and its descendants."""
    AGENT_TYPE_HUMAN = 'human'
    AGENT_TYPE_MACHINE = 'machine'
    AGENT_TYPE_UNKNOWN = 'unknown'
    AGENT_TYPE_CHOICES = [
        (AGENT_TYPE_HUMAN, 'Human'),
        (AGENT_TYPE_MACHINE, 'Machine'),
        (AGENT_TYPE_UNKNOWN, 'Unknown'),
    ]
    EVENT_TYPE_CANCELLED = 'cancelled'
    EVENT_TYPE_CREATED = 'created'
    EVENT_TYPE_DELETED = 'deleted'
    EVENT_TYPE_DERIVED = 'derived'
    EVENT_TYPE_REVISED = 'revised'
    EVENT_TYPE_UNKNOWN = 'unknown'
    EVENT_TYPE_UPDATED = 'updated'
    EVENT_TYPE_CHOICES = [
        (EVENT_TYPE_CANCELLED, 'Cancelled'),
        (EVENT_TYPE_CREATED, 'Created'),
        (EVENT_TYPE_DELETED, 'Deleted'),
        (EVENT_TYPE_DERIVED, 'Derived'),
        (EVENT_TYPE_REVISED, 'Revised'),
        (EVENT_TYPE_UNKNOWN, 'Unknown'),
        (EVENT_TYPE_UPDATED, 'Updated'),
    ]
    maintenancehistory = models.ForeignKey(EAD, on_delete=models.CASCADE)
    agent_altrender = deepcopy(altrender)
    agent_audience = deepcopy(audience)
    agent_encodinganalog = deepcopy(encodinganalog)
    agent_ead_id = deepcopy(ead_id)
    agent_lang = deepcopy(lang)
    agent_script = deepcopy(script)
    agent = models.CharField(max_length=128)
    agenttype_altrender = deepcopy(altrender)
    agenttype_audience = deepcopy(audience)
    agenttype_encodinganalog = deepcopy(encodinganalog)
    agenttype_ead_id = deepcopy(ead_id)
    agenttype_lang = deepcopy(lang)
    agenttype_script = deepcopy(script)
    agenttype_value = models.CharField(
        choices=AGENT_TYPE_CHOICES, max_length=7)
    agenttype = models.CharField(blank=True, max_length=32)
    eventdatetime_altrender = deepcopy(altrender)
    eventdatetime_audience = deepcopy(audience)
    eventdatetime_encodinganalog = deepcopy(encodinganalog)
    eventdatetime_ead_id = deepcopy(ead_id)
    eventdatetime_lang = deepcopy(lang)
    eventdatetime_script = deepcopy(script)
    eventdatetime_standarddatetime = models.CharField(
        blank=True, max_length=25, validators=[validate_date_time])
    eventdatetime = models.CharField(blank=True, max_length=128)
    eventtype_altrender = deepcopy(altrender)
    eventtype_audience = deepcopy(audience)
    eventtype_encodinganalog = deepcopy(encodinganalog)
    eventtype_ead_id = deepcopy(ead_id)
    eventtype_lang = deepcopy(lang)
    eventtype_script = deepcopy(script)
    eventtype_value = models.CharField(
        choices=EVENT_TYPE_CHOICES, max_length=9)
    eventtype = models.CharField(blank=True, max_length=32)


@reversion.register()
class MaterialSpec(CommonMixin, EncodingAnalogMixin, LabelMixin,
                   LangScriptMixin, LocalTypeMixin):
    """Corresponds to EAD3 materialspec."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)
    materialspec = models.TextField()


@reversion.register(follow=['part_set'])
class Name(AccessMixin, CommonMixin, EncodingAnalogMixin, LangScriptMixin,
           LocalTypeMixin, NormalMixin, RelatorMixin, NameMixin):
    """Corresponds to EAD3 name."""
    pass


@reversion.register()
class NamePart(PartMixin):
    """Corresponds to EAD3 part as a child of name."""
    name = models.ForeignKey(
        Name, on_delete=models.CASCADE, related_name='part_set')

    class Meta:
        ordering = ['order']
        unique_together = ['name', 'order']


@reversion.register()
class ODD(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
          LocalTypeMixin):
    """Corresponds to EAD3 odd."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    odd = models.TextField()


@reversion.register()
class OriginalsLoc(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                   LocalTypeMixin):
    """Corresponds to EAD3 originalsloc."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    originalsloc = models.TextField()


@reversion.register()
class Origination(CommonMixin, EncodingAnalogMixin, LabelMixin,
                  LangScriptMixin, LocalTypeMixin):
    """Corresponds to EAD3 origination."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)
    corpnames = models.ManyToManyField(CorpName, blank=True)
    famnames = models.ManyToManyField(FamName, blank=True)
    names = models.ManyToManyField(Name, blank=True)
    persnames = models.ManyToManyField('PersName', blank=True)

    def clean(self):
        # There must be at least one CorpName, FamnName, Name, or
        # PersName associated with an Origination. Since these are
        # many to many fields, we must be able to create an
        # Origination instance before populating them, so do not run
        # this validation if there is no primary key.
        if self.pk is None:
            return
        if self.corpnames.count() + self.famnames.count() + \
                self.names.count() + self.persnames.count() == 0:
            raise ValidationError(
                'Origination must reference at least one named entity.')


@reversion.register()
class OtherAgencyCode(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                      LocalTypeMixin):
    """Corresponds to EAD3 otheragencycode."""
    maintenanceagency = models.ForeignKey(EAD, on_delete=models.CASCADE)
    otheragencycode = models.CharField(max_length=32)


@reversion.register()
class OtherFindAid(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                   LocalTypeMixin):
    """Corresponds to EAD3 otherfindaid."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    otherfindaid = models.TextField()


@reversion.register()
class OtherRecordID(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                    LocalTypeMixin):
    """Corresponds to EAD3 otherrecordid."""
    control = models.ForeignKey(EAD, on_delete=models.CASCADE)
    otherrecordid = models.CharField(max_length=512)


@reversion.register(follow=['part_set'])
class PersName(AccessMixin, CommonMixin, EncodingAnalogMixin, LangScriptMixin,
               LocalTypeMixin, NormalMixin, RelatorMixin, NameMixin):
    """Corresponds to EAD3 persname."""
    pass


@reversion.register()
class PersNamePart(PartMixin):
    """Corresponds to EAD3 part as a child of persname."""
    name = models.ForeignKey(
        PersName, on_delete=models.CASCADE, related_name='part_set')

    class Meta:
        ordering = ['order']
        unique_together = ['name', 'order']


@reversion.register()
class PhysDesc(CommonMixin, EncodingAnalogMixin, LabelMixin, LangScriptMixin,
               LocalTypeMixin):
    """Corresponds to EAD3 physdesc."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)
    physdesc = models.TextField()


@reversion.register(follow=['physdescstructured_set'])
class PhysDescSet(CommonMixin, CoverageMixin, EncodingAnalogMixin, LabelMixin,
                  LangScriptMixin, DescriptiveNoteMixin):
    """Corresponds to EAD3 physdescset."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)
    parallel = models.BooleanField(blank=True, null=True)


@reversion.register(follow=['dimensions_set', 'physfacet_set'])
class PhysDescSetPhysDescStructured(PhysDescStructuredMixin):
    """Corresponds to EAD3 physdescstructured as a child of physdescset."""
    parent = models.ForeignKey(
        PhysDescSet, on_delete=models.CASCADE,
        related_name='physdescstructured_set')


@reversion.register()
class PhysDescSetPhyDescStructuredDimensions(DimensionsMixin):
    """Corresponds to EAD3 dimensions as a grandchild of physdescset."""
    physdescstructured = models.ForeignKey(
        PhysDescSetPhysDescStructured, on_delete=models.CASCADE,
        related_name='dimensions_set')


@reversion.register()
class PhysDescSetPhysDescStructuredPhysFacet(PhysFacetMixin):
    """Corresponds to EAD3 physfacet as a grandchild of physdescset."""
    physdescstructured = models.ForeignKey(
        PhysDescSetPhysDescStructured, on_delete=models.CASCADE,
        related_name='physfacet_set')


@reversion.register()
class PhysLoc(CommonMixin, EncodingAnalogMixin, LabelMixin, LangScriptMixin,
              LocalTypeMixin):
    """Corresponds to EAD3 physloc."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)
    parents = models.ManyToManyField(
        'self', blank=True, related_name='child_physlocs', symmetrical=False)
    physloc = models.TextField()


@reversion.register()
class PhysTech(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
               LocalTypeMixin):
    """Corresponds to EAD3 phystech."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    phystech = models.TextField()


@reversion.register()
class PreferCite(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                 LocalTypeMixin):
    """Corresponds to EAD3 prefercite."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    prefercite = models.TextField()


@reversion.register()
class ProcessInfo(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                  LocalTypeMixin):
    """Corresponds to EAD3 processinfo."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    processinfo = models.TextField()


@reversion.register()
class RelatedMaterial(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                      LocalTypeMixin):
    """Corresponds to EAD3 relatedmaterial."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    relatedmaterial = models.TextField()


@reversion.register(follow=['daterange_set', 'datesingle_set',
                            'relationentry_set'])
class Relation(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
               LinkMixin, DateSetMixin, DescriptiveNoteMixin,
               ObjectXMLWrapMixin):
    """Corresponds to EAD3 relation."""
    RELATION_TYPE_CPF = 'cpfrelation'
    RELATION_TYPE_FUNCTION = 'functionrelation'
    RELATION_TYPE_RESOURCE = 'resourcerelation'
    RELATION_TYPE_OTHER = 'otherrelationtype'
    RELATION_TYPE_CHOICES = [
        (RELATION_TYPE_CPF, 'CPF'),
        (RELATION_TYPE_FUNCTION, 'Function'),
        (RELATION_TYPE_RESOURCE, 'Resource'),
        (RELATION_TYPE_OTHER, 'Other'),
    ]
    relations = models.ForeignKey(EAD, on_delete=models.CASCADE)
    lastdatetimeverified = deepcopy(lastdatetimeverified)
    otherrelationtype = models.CharField(
        blank=True, max_length=64, validators=[validate_token])
    relationtype = models.CharField(
        choices=RELATION_TYPE_CHOICES, max_length=17)
    geogname_altrender = deepcopy(altrender)
    geogname_audience = deepcopy(audience)
    geogname_encodinganalog = deepcopy(encodinganalog)
    geogname_ead_id = deepcopy(ead_id)
    geogname_identifier = deepcopy(identifier)
    geogname_lang = deepcopy(lang)
    geogname_localtype = deepcopy(localtype)
    geogname_normal = deepcopy(normal)
    geogname_relator = deepcopy(relator)
    geogname_rules = deepcopy(rules)
    geogname_script = deepcopy(script)
    geogname_source = deepcopy(source)
    geogname = models.TextField(blank=True)


@reversion.register()
class RelationDateRange(DateRangeMixin):
    """Corresponds to EAD3 daterange as a child of relation."""
    parent = models.ForeignKey(
        Relation, on_delete=models.CASCADE, related_name='daterange_set')


@reversion.register()
class RelationDateSingle(DateSingleMixin):
    """Corresponds to EAD3 datesingle as a child of relation."""
    parent = models.ForeignKey(
        Relation, on_delete=models.CASCADE, related_name='datesingle_set')


@reversion.register()
class RelationEntry(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                    LocalTypeMixin, TransliterationMixin):
    """Corresponds to EAD3 relationentry."""
    relation = models.ForeignKey(Relation, on_delete=models.CASCADE)
    relationentry = models.TextField()


@reversion.register(follow=['addressline_set'])
class Repository(CommonMixin, EncodingAnalogMixin, LabelMixin, LangScriptMixin,
                 LocalTypeMixin):
    """Corresponds to EAD3 repository."""
    address_altrender = deepcopy(altrender)
    address_audience = deepcopy(audience)
    address_ead_id = deepcopy(ead_id)
    address_lang = deepcopy(lang)
    address_script = deepcopy(script)
    assembled_name = models.TextField(blank=True)
    corpnames = models.ManyToManyField(CorpName, blank=True)
    famnames = models.ManyToManyField(FamName, blank=True)
    names = models.ManyToManyField(Name, blank=True)
    persnames = models.ManyToManyField(PersName, blank=True)

    def clean(self):
        # There must be at least one CorpName, FamnName, Name, or
        # PersName associated with a Repository. Since these are
        # many to many fields, we must be able to create an
        # Repository instance before populating them, so do not run
        # this validation if there is no primary key.
        if self.pk is None:
            return
        if self.corpnames.all().count() + self.famnames.all().count() + \
           self.names.all().count() + self.persnames.all().count() == 0:
            raise ValidationError(
                'Repository must reference at least one named entity.')

    def save(self, *args, **kwargs):
        # Populate the assembled_name field from data drawn from all
        # associated *Name objects.
        if self.pk:
            name_parts = []
            name_parts.extend(
                self.corpnames.values_list('assembled_name', flat=True))
            name_parts.extend(
                self.famnames.values_list('assembled_name', flat=True))
            name_parts.extend(self.names.values_list(
                'assembled_name', flat=True))
            name_parts.extend(
                self.persnames.values_list('assembled_name', flat=True))
            self.assembled_name = '; '.join(name_parts)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.assembled_name


@reversion.register()
class RepositoryAddressLine(CommonMixin, LangScriptMixin, LocalTypeMixin):
    """Corresponds to EAD3 addressline as a grandchild of repository."""
    address = models.ForeignKey(
        Repository, on_delete=models.CASCADE, related_name='addressline_set')
    addressline = models.TextField()


@reversion.register()
class Representation(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                     LinkMixin, LocalTypeMixin):
    """Corresponds to EAD3 representation."""
    control = models.ForeignKey(EAD, on_delete=models.CASCADE)
    representation = models.TextField(blank=True)


@reversion.register()
class RightsDeclaration(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                        LocalTypeMixin, AbbrMixin, CitationMixin,
                        DescriptiveNoteMixin):
    """Corresponds to EAD3 rightsdeclaration."""
    control = models.ForeignKey(EAD, on_delete=models.CASCADE)


@reversion.register()
class ScopeContent(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                   LocalTypeMixin):
    """Corresponds to EAD3 scopecontent."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    scopecontent = models.TextField()


@reversion.register()
class SeparatedMaterial(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                        LocalTypeMixin):
    """Corresponds to EAD3 separatedmaterial."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    separatedmaterial = models.TextField()


@reversion.register(follow=['sourceentry_set'])
class Source(CommonMixin, EncodingAnalogMixin, LangScriptMixin, LinkMixin,
             DescriptiveNoteMixin, ObjectXMLWrapMixin):
    """Corresponds to EAD3 source."""
    sources = models.ForeignKey(EAD, on_delete=models.CASCADE)
    lastdatetimeverified = deepcopy(lastdatetimeverified)


@reversion.register()
class SourceEntry(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                  TransliterationMixin):
    """Corresponds to EAD3 sourceentry."""
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    sourceentry = models.TextField()


@reversion.register()
class Sponsor(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
              LocalTypeMixin):
    """Corresponds to EAD3 sponsor."""
    titlestmt = models.ForeignKey(EAD, on_delete=models.CASCADE)
    sponsor = models.TextField()


@reversion.register()
class Subtitle(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
               LocalTypeMixin):
    """Corresponds to EAD3 subtitle."""
    titlestmt = models.ForeignKey(EAD, on_delete=models.CASCADE)
    subtitle = models.TextField()


@reversion.register()
class TitleProper(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                  LocalTypeMixin):
    """Corresponds to EAD3 titleproper as a child of titlestmt.

    titleproper must also occur in EAD3 as a child of seriesstmt, but
    all of seriesstmt is held as serialised XML and not in individual
    fields.

    """
    RENDER_ALTRENDER = 'altrender'
    RENDER_BOLD = 'bold'
    RENDER_BOLDDOUBLEQUOTE = 'bolddoublequote'
    RENDER_BOLDITALIC = 'bolditalic'
    RENDER_BOLDSINGLEQUOTE = 'boldsinglequote'
    RENDER_BOLDSMCAPS = 'boldsmcaps'
    RENDER_BOLDUNDERLINE = 'boldunderline'
    RENDER_DOUBLEQUOTE = 'doublequote'
    RENDER_ITALIC = 'italic'
    RENDER_NONPROPORT = 'nonproport'
    RENDER_SINGLEQUOTE = 'singlequote'
    RENDER_SMCAPS = 'smcaps'
    RENDER_SUB = 'sub'
    RENDER_SUPER = 'super'
    RENDER_UNDERLINE = 'underline'
    RENDER_CHOICES = [
        (RENDER_ALTRENDER, 'Alternative rendering'),
        (RENDER_BOLD, 'Bold'),
        (RENDER_BOLDDOUBLEQUOTE, 'Bold double quote'),
        (RENDER_BOLDITALIC, 'Bold italic'),
        (RENDER_BOLDSINGLEQUOTE, 'Bold single quote'),
        (RENDER_BOLDSMCAPS, 'Bold small caps'),
        (RENDER_BOLDUNDERLINE, 'Bold underline'),
        (RENDER_DOUBLEQUOTE, 'Double quote'),
        (RENDER_ITALIC, 'Italic'),
        (RENDER_NONPROPORT, 'Non-proportional'),
        (RENDER_SINGLEQUOTE, 'Single quote'),
        (RENDER_SMCAPS, 'Small caps'),
        (RENDER_SUB, 'Subscript'),
        (RENDER_SUPER, 'Superscript'),
        (RENDER_UNDERLINE, 'Underline'),
    ]
    titlestmt = models.ForeignKey(EAD, on_delete=models.CASCADE)
    titleproper = models.TextField()
    render = models.CharField(
        blank=True, choices=RENDER_CHOICES, max_length=15)


@reversion.register()
class UnitDate(CommonMixin, EncodingAnalogMixin, LabelMixin, LangScriptMixin,
               NormalMixin, UnitDateAttrMixin):
    """Corresponds to EAD3 unitdate."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)
    unitdate = models.TextField()


@reversion.register(follow=['daterange_set', 'datesingle_set'])
class UnitDateStructured(CommonMixin, EncodingAnalogMixin, LabelMixin,
                         LangScriptMixin, UnitDateAttrMixin, DateSetMixin):
    """Corresponds to EAD3 unitdatestructured."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)


@reversion.register()
class UnitDateStructuredDateRange(DateRangeMixin):
    """Corresponds to EAD3 daterange as a child or grandchild (within
    dateset) of unitdatestructured."""
    parent = models.ForeignKey(
        UnitDateStructured, on_delete=models.CASCADE,
        related_name='daterange_set')


@reversion.register()
class UnitDateStructuredDateSingle(DateSingleMixin):
    """Corresponds to EAD3 datesingle as a child or grandchild (within
    dateset) of unitdatestructured."""
    parent = models.ForeignKey(
        UnitDateStructured, on_delete=models.CASCADE,
        related_name='datesingle_set')


@reversion.register()
class UnitId(CommonMixin, EncodingAnalogMixin, LabelMixin, LangScriptMixin,
             LocalTypeMixin):
    """Corresponds to EAD3 unitid."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)
    unitid = models.TextField()
    countrycode = deepcopy(countrycode)
    identifier = deepcopy(identifier)
    repositorycode = models.CharField(
        blank=True, max_length=32, validators=[validate_token])


@reversion.register()
class UnitTitle(CommonMixin, EncodingAnalogMixin, LabelMixin, LangScriptMixin,
                LocalTypeMixin, NormalMixin):
    """Corresponds to EAD3 unittitle."""
    did = models.ForeignKey(EAD, on_delete=models.CASCADE)
    unittitle = models.TextField()


@reversion.register()
class UseRestrict(CommonMixin, EncodingAnalogMixin, LangScriptMixin,
                  LocalTypeMixin):
    """Corresponds to EAD3 userestrict."""
    archdesc = models.ForeignKey(EAD, on_delete=models.CASCADE)
    userestrict = models.TextField()
