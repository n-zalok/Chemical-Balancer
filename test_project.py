from project import get_side, balance, factorize, generate_side
import pytest

def test_get_side():
    assert get_side('CO2+H2O') == [{'C': 1, 'O': 2}, {'O': 1, 'H': 2}]
    assert get_side('C6H12O6+O2') == [{'O': 2}, {'C': 6, 'H': 12, 'O': 6}]
    assert get_side('Al+HCl') == [{'Al': 1}, {'H': 1, 'Cl': 1}]
    assert get_side('AlCl3+H2') == [{'H': 2}, {'Al': 1, 'Cl': 3}]
    assert get_side('Fe2(SO4)3+KOH') == [{'S': 3, 'Fe': 2, 'O': 12}, {'K': 1, 'O': 1, 'H': 1}]
    assert get_side('K2SO4+Fe(OH)3') == [{'S': 1, 'K': 2, 'O': 4}, {'Fe': 1, 'O': 3, 'H': 3}]
    with pytest.raises(ValueError):
        assert get_side('HELLO THIS IS CS50')
        assert get_side('Na+cl')
        assert get_side('co+HCl')


def test_balance():
    assert balance([{'C': 1, 'O': 2}, {'O': 1, 'H': 2}], [{'O': 2}, {'C': 6, 'H': 12, 'O': 6}]) == ({6.0: {'C': 1, 'O': 2}, 6.001: {'O': 1, 'H': 2}}, {6.0: {'O': 2}})
    assert balance([{'Al': 1}, {'H': 1, 'Cl': 1}], [{'H': 2}, {'Al': 1, 'Cl': 3}]) == ({3.0: {'H': 1, 'Cl': 1}}, {1.5: {'H': 2}})
    assert balance([{'S': 3, 'Fe': 2, 'O': 12}, {'K': 1, 'O': 1, 'H': 1}], [{'S': 1, 'K': 2, 'O': 4}, {'Fe': 1, 'O': 3, 'H': 3}]) == ({6.0: {'K': 1, 'O': 1, 'H': 1}}, {3.0: {'S': 1, 'K': 2, 'O': 4}, 2.0: {'Fe': 1, 'O': 3, 'H': 3}})


def test_factorize():
    assert factorize({6.0: {'C': 1, 'O': 2}, 6.001: {'O': 1, 'H': 2}}, {6.0: {'O': 2}}, [{'C': 1, 'O': 2}, {'O': 1, 'H': 2}], [{'O': 2}, {'C': 6, 'H': 12, 'O': 6}]) == ({6.0: {'C': 1, 'O': 2}, 6.001: {'O': 1, 'H': 2}}, {6.0: {'O': 2}}, 1)
    assert factorize({3.0: {'H': 1, 'Cl': 1}}, {1.5: {'H': 2}}, [{'Al': 1}, {'H': 1, 'Cl': 1}], [{'H': 2}, {'Al': 1, 'Cl': 3}]) == ({6.0: {'H': 1, 'Cl': 1}}, {3.0: {'H': 2}}, 2)
    assert factorize({6.0: {'K': 1, 'O': 1, 'H': 1}}, {3.0: {'S': 1, 'K': 2, 'O': 4}, 2.0: {'Fe': 1, 'O': 3, 'H': 3}}, [{'S': 3, 'Fe': 2, 'O': 12}, {'K': 1, 'O': 1, 'H': 1}], [{'S': 1, 'K': 2, 'O': 4}, {'Fe': 1, 'O': 3, 'H': 3}]) == ({6.0: {'K': 1, 'O': 1, 'H': 1}}, {3.0: {'S': 1, 'K': 2, 'O': 4}, 2.0: {'Fe': 1, 'O': 3, 'H': 3}}, 1)


def test_generate_side():
    assert generate_side({6.0: {'C': 1, 'O': 2}, 6.001: {'O': 1, 'H': 2}}, 'CO2+H2O', 1) == '6CO2 + 6H2O = '
    assert generate_side({6.0: {'O': 2}}, 'C6H12O6+O2', 1) == 'C6H12O6 + 6O2 = '
    assert generate_side({6.0: {'H': 1, 'Cl': 1}}, 'Al+HCl', 2) == '2Al + 6HCl = '
    assert generate_side({3.0: {'H': 2}}, 'AlCl3+H2', 2) == '2AlCl3 + 3H2 = '
    assert generate_side({6.0: {'K': 1, 'O': 1, 'H': 1}}, 'Fe2(SO4)3+KOH', 1) == 'Fe2(SO4)3 + 6KOH = '
    assert generate_side({3.0: {'S': 1, 'K': 2, 'O': 4}, 2.0: {'Fe': 1, 'O': 3, 'H': 3}}, 'K2SO4+Fe(OH)3', 1) == '3K2SO4 + 2Fe(OH)3 = '
