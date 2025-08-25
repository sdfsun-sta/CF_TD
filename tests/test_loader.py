from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
import pytest

from data_loader import load_weapons


def test_load_weapons_valid():
    weapons = load_weapons(Path('data/Weapon.csv'))
    assert len(weapons) == 2
    assert weapons[0].Id == 'AR'


def test_load_weapons_invalid(tmp_path):
    csv_path = tmp_path / 'Weapon.csv'
    csv_path.write_text(
        'Id,Slot,Type,BaseDamage,HeadshotMult,CritMult,DistanceFalloff,ArmorPen,FireRate,Mag,Reload,RefireCD,Range,BulletSpeed,AccBase,AccS,AccK,acc_floor,WeakpointRate_Near,WeakpointRate_Mid,WeakpointRate_Far,TurnRate,MultiLock,pierce_cnt,hit_limit,AOERadius,SplashCurveId,Tags\n'
        'Bad,Primary,AR,28,2.5,1.2,0.5,1.2,8.5,30,2.0,,100,900,0.2,6,0.03,0.1,0.1,0.2,0.3,90,1,0,1,0,,default\n'
    )
    with pytest.raises(ValueError):
        load_weapons(csv_path)
