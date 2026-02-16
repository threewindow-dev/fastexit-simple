"""Unit tests for Institution domain model."""

import pytest

from subdomains.portfolio.domain.errors import InvalidStateError
from subdomains.portfolio.domain.models import Institution


class TestInstitutionModel:
    def test_create_institution_with_valid_type(self):
        institution = Institution.create(name="KB증권", type="증권사", display_order=1)

        assert institution.institution_id is None
        assert institution.name == "KB증권"
        assert institution.type == "증권사"
        assert institution.display_order == 1

    def test_create_institution_with_bank_type(self):
        institution = Institution.create(name="국민은행", type="은행")

        assert institution.type == "은행"

    def test_invalid_type_raises_error(self):
        with pytest.raises(InvalidStateError):
            Institution.create(name="테스트", type="기타")

    def test_negative_display_order_raises_error(self):
        with pytest.raises(InvalidStateError):
            Institution.create(name="테스트", type="증권사", display_order=-1)
