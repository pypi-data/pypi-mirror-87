"""Regression tests for reading sd24bits.grib."""

import numpy


gribfile = "data/sd24bits.grib"


class TestIndicatorSection:

    section_number = 0
    fieldnames = {"identifier", "editionNumber", "totalLength"}

    def test_fieldnames(self, section):
        assert section.fieldnames == self.fieldnames

    def test_identifier(self, section):
        assert section.identifier == b"GRIB"

    def test_totalLength(self, section):
        assert section.totalLength == 6804

    def test_editionNumber(self, section):
        assert section.editionNumber == 1


class TestProductDefinitionSection:

    section_number = 1
    fieldnames = {
        "section1Length",
        "table2Version",
        "centre",
        "generatingProcessIdentifier",
        "gridDefinition",
        "section1Flags",
        "indicatorOfParameter",
        "indicatorOfTypeOfLevel",
        "level",
        "localDefinitionNumber",
        "yearOfCentury",
        "month",
        "day",
        "hour",
        "minute",
        "unitOfTimeRange",
        "P1",
        "P2",
        "timeRangeIndicator",
        "numberIncludedInAverage",
        "numberMissingFromAveragesOrAccumulations",
        "centuryOfReferenceTimeOfData",
        "subCentre",
        "decimalScaleFactor",
    }

    def test_fieldnames(self, section):
        assert section.fieldnames == self.fieldnames

    def test_section1Length(self, section):
        assert section.section1Length == 52

    def test_table2Version(self, section):
        assert section.table2Version == 128

    def test_centre(self, section):
        assert section.centre == 98

    def test_generatingProcessIdentifier(self, section):
        assert section.generatingProcessIdentifier == 255

    def test_gridDefinition(self, section):
        assert section.gridDefinition == 255

    def test_section1Flags(self, section):
        assert section.section1Flags == 128

    def test_indicatorOfParameter(self, section):
        assert section.indicatorOfParameter == 141

    def test_indicatorOfTypeOfLevel(self, section):
        assert section.indicatorOfTypeOfLevel == 1

    def test_level(self, section):
        assert section.level == 0

    def test_yearOfCentury(self, section):
        assert section.yearOfCentury == 79

    def test_month(self, section):
        assert section.month == 12

    def test_day(self, section):
        assert section.day == 1

    def test_hour(self, section):
        assert section.hour == 0

    def test_minute(self, section):
        assert section.minute == 0

    def test_unitOfTimeRange(self, section):
        assert section.unitOfTimeRange == 1

    def test_P1(self, section):
        assert section.P1 == 0

    def test_P2(self, section):
        assert section.P2 == 6

    def test_timeRangeIndicator(self, section):
        assert section.timeRangeIndicator == 123

    def test_numberIncludedInAverage(self, section):
        assert section.numberIncludedInAverage == 124

    def test_numberMissingFromAveragesOrAccumulations(self, section):
        assert section.numberMissingFromAveragesOrAccumulations == 0

    def test_centuryOfReferenceTimeOfData(self, section):
        assert section.centuryOfReferenceTimeOfData == 20

    def test_subCentre(self, section):
        assert section.subCentre == 0

    def test_decimalScaleFactor(self, section):
        assert section.decimalScaleFactor == 0


class TestGridDescriptionSection:

    section_number = 2
    fieldnames = {
        "section2Length",
        "numberOfVerticalCoordinateValues",
        "pvlLocation",
        "dataRepresentationType",
        "Ni",
        "Nj",
        "latitudeOfFirstGridPoint",
        "longitudeOfFirstGridPoint",
        "resolutionAndComponentFlags",
        "latitudeOfLastGridPoint",
        "longitudeOfLastGridPoint",
        "iDirectionIncrement",
        "jDirectionIncrement",
        "scanningMode",
    }

    def test_fieldnames(self, section):
        assert section.fieldnames == self.fieldnames

    def test_section2Length(self, section):
        assert section.section2Length == 32

    def test_numberOfVerticalCoordinateValues(self, section):
        assert section.numberOfVerticalCoordinateValues == 0

    def test_pvlLocation(self, section):
        assert section.pvlLocation == 255

    def test_dataRepresentationType(self, section):
        assert section.dataRepresentationType == 0

    def test_Ni(self, section):
        assert section.Ni == 360 // 5

    def test_Nj(self, section):
        assert section.Nj == 90 // 3 + 1

    def test_latitudeOfFirstGridPoint(self, section):
        assert section.latitudeOfFirstGridPoint == 90000

    def test_longitudeOfFirstGridPoint(self, section):
        assert section.longitudeOfFirstGridPoint == -180000

    def test_resolutionAndComponentFlags(self, section):
        assert section.resolutionAndComponentFlags == 128

    def test_latitudeOfLastGridPoint(self, section):
        assert section.latitudeOfLastGridPoint == 0

    def test_longitudeOfLastGridPoint(self, section):
        assert section.longitudeOfLastGridPoint == 175000

    def test_iDirectionIncrement(self, section):
        assert section.iDirectionIncrement == 5000

    def test_jDirectionIncrement(self, section):
        assert section.jDirectionIncrement == 3000

    def test_scanningMode(self, section):
        assert section.scanningMode == 0


class TestBinaryDataSection:

    section_number = 4
    fieldnames = {
        "section4Length",
        "dataFlag",
        "binaryScaleFactor",
        "referenceValue",
        "bitsPerValue",
        "values",
    }

    def test_fieldnames(self, section):
        assert section.fieldnames == self.fieldnames

    def test_section4Length(self, section):
        assert section.section4Length == 6708

    def test_dataFlag(self, section):
        assert section.dataFlag == 8

    def test_binaryScaleFactor(self, section):
        assert section.binaryScaleFactor == -20

    def test_referenceValue(self, section):
        assert section.referenceValue == 0.0

    def test_bitsPerValue(self, section):
        assert section.bitsPerValue == 24

    def test_values(self, section):
        assert len(section.values) == 31 * 72
        assert section.values.dtype == numpy.uint32
        assert section.values.max() == 10 * (1 << 20)


class TestEndSection:

    section_number = 5
    fieldnames = {"endOfMessage"}

    def test_fieldnames(self, section):
        assert section.fieldnames == self.fieldnames

    def test_endOfMessage(self, section):
        assert section.endOfMessage == b"7777"
