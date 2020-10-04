import sys
import json
import os
import io
import re
import boolean
import itertools
from bitarray import bitarray

def parseFunctions(rule):
    srule = rule.strip()
    srule = srule.replace('can_use(Dins_Fire)','(Dins_Fire and Magic_Meter)')
    srule = srule.replace('can_use(Hookshot)','(is_adult and Hookshot)')
    srule = srule.replace('can_use(Bow)','(is_adult and Bow)')
    srule = srule.replace('can_use(Slingshot)','(is_child and Slingshot)')
    srule = srule.replace('can_use(Boomerang)','(is_child and Boomerang)')
    srule = srule.replace('has_sticks','Deku_Sticks')
    srule = srule.replace('has_nuts','Deku_Nuts')
    srule = srule.replace('has_explosives','(Bomb_Bag or (Bombchus and chus_in_logic))')
    srule = srule.replace('can_blast_or_smash','(Bomb_Bag or (Bombchus and chus_in_logic) or (Hammer and is_adult))')
    srule = srule.replace('here(','(')
    srule = srule.replace('can_child_attack','(Slingshot or Boomerang or Deku_Sticks or Bomb_Bag or (Bombchus and chus_in_logic) or Kokiri_Sword or (Dins_Fire and Magic_Meter))')
    srule = srule.replace('can_use_projectile','((Bomb_Bag or (Bombchus and chus_in_logic)) or (is_child and (Slingshot or Boomerang)) or (is_adult and (Bow or Hookshot)))')
    srule = srule.replace('has_fire_source_with_torch','((Dins_Fire and Magic_Meter) or (Bow and Fire_Arrows and Magic_Meter and is_adult) or (is_child and Deku_Sticks))')
    srule = srule.replace('has_fire_source','((Dins_Fire and Magic_Meter) or (Bow and Fire_Arrows and Magic_Meter and is_adult))')
    srule = srule.replace('has_slingshot','Slingshot')
    srule = srule.replace('has_shield','((is_child and Deku_Shield) or (is_adult and Hylian_Shield))')
    srule = srule.replace('can_play(Zeldas_Lullaby)','(Ocarina and Zeldas_Lullaby)')
    srule = srule.replace('can_play(Eponas_Song)','(Ocarina and Eponas_Song)')
    srule = srule.replace('can_play(Sarias_Song)','(Ocarina and Sarias_Song)')
    srule = srule.replace('can_play(Suns_Song)','(Ocarina and Suns_Song)')
    srule = srule.replace('can_play(Song_of_Time)','(Ocarina and Song_of_Time)')
    srule = srule.replace('can_play(Song_of_Storms)','(Ocarina and Song_of_Storms)')
    srule = srule.replace('can_play(Minuet_of_Forest)','(Ocarina and Minuet)')
    srule = srule.replace('can_play(Bolero_of_Fire)','(Ocarina and Bolero)')
    srule = srule.replace('can_play(Serenade_of_Water)','(Ocarina and Serenade)')
    srule = srule.replace('can_play(Requiem_of_Spirit)','(Ocarina and Requiem)')
    srule = srule.replace('can_play(Nocturne_of_Shadow)','(Ocarina and Nocturne)')
    srule = srule.replace('can_play(Prelude_of_Light)','(Ocarina and Prelude)')
    srule = srule.replace('can_use(Hover_Boots)','(is_adult and Hover_Boots)')
    srule = srule.replace("'Links Cow'",'Links_Cow_Obtained')
    srule = srule.replace('can_use(Longshot)','(is_adult and Longshot)')
    srule = srule.replace("shuffle_scrubs == 'off'",'(not_scrubsanity)')
    srule = srule.replace('can_use(Sticks)','(is_child and Deku_Sticks)')
    srule = srule.replace('can_use(Epona)','(is_adult and Ocarina and Eponas_Song and Epona)')
    srule = srule.replace('can_use(Scarecrow)','(is_adult and Ocarina and Scarecrow_Song and Hookshot)')
    srule = srule.replace('can_use(Distant_Scarecrow)','(is_adult and Ocarina and Scarecrow_Song and Longshot)')
    srule = srule.replace("'Water Temple Clear'",'Water_Temple_Clear')
    srule = srule.replace("(Progressive_Scale, 2)",'Gold_Scale')
    srule = srule.replace('can_use(Hammer)','(is_adult and Hammer)')
    srule = srule.replace("lacs_condition == 'vanilla'",'lacs_vanilla')
    srule = srule.replace("lacs_condition == 'medallions'",'lacs_medallions')
    srule = srule.replace("lacs_condition == 'stones'",'lacs_stones')
    srule = srule.replace("lacs_condition == 'dungeons'",'lacs_ad')
    srule = srule.replace("(Bottle_with_Big_Poe, big_poe_count)",'((Bottle_with_Big_Poe1 and big_poes1) or (Bottle_with_Big_Poe1 and Bottle_with_Big_Poe2 and big_poes2) or (Bottle_with_Big_Poe1 and Bottle_with_Big_Poe2 and Bottle_with_Big_Poe3 and big_poes3) or (Bottle_with_Big_Poe1 and Bottle_with_Big_Poe2 and Bottle_with_Big_Poe3 and Bottle_with_Big_Poe4 and big_poes4))')
    srule = srule.replace('can_use(Lens_of_Truth)','(Magic_Meter and Lens_of_Truth)')
    srule = srule.replace("damage_multiplier != 'ohko'",'not_ohko')
    srule = srule.replace('can_use(Nayrus_Love)','(Magic_Meter and Nayrus_Love)')
    srule = srule.replace('(Gold_Skulltula_Token, 10)','(Gold_Skulltula_001 and Gold_Skulltula_002 and Gold_Skulltula_003 and Gold_Skulltula_004 and Gold_Skulltula_005 and Gold_Skulltula_006 and Gold_Skulltula_007 and Gold_Skulltula_008 and Gold_Skulltula_009 and Gold_Skulltula_010)')
    srule = srule.replace('(Gold_Skulltula_Token, 20)','(Gold_Skulltula_001 and Gold_Skulltula_002 and Gold_Skulltula_003 and Gold_Skulltula_004 and Gold_Skulltula_005 and Gold_Skulltula_006 and Gold_Skulltula_007 and Gold_Skulltula_008 and Gold_Skulltula_009 and Gold_Skulltula_010 and Gold_Skulltula_011 and Gold_Skulltula_012 and Gold_Skulltula_013 and Gold_Skulltula_014 and Gold_Skulltula_015 and Gold_Skulltula_016 and Gold_Skulltula_017 and Gold_Skulltula_018 and Gold_Skulltula_019 and Gold_Skulltula_020)')
    srule = srule.replace('(Gold_Skulltula_Token, 30)','(Gold_Skulltula_001 and Gold_Skulltula_002 and Gold_Skulltula_003 and Gold_Skulltula_004 and Gold_Skulltula_005 and Gold_Skulltula_006 and Gold_Skulltula_007 and Gold_Skulltula_008 and Gold_Skulltula_009 and Gold_Skulltula_010 and Gold_Skulltula_011 and Gold_Skulltula_012 and Gold_Skulltula_013 and Gold_Skulltula_014 and Gold_Skulltula_015 and Gold_Skulltula_016 and Gold_Skulltula_017 and Gold_Skulltula_018 and Gold_Skulltula_019 and Gold_Skulltula_020 and Gold_Skulltula_021 and Gold_Skulltula_022 and Gold_Skulltula_023 and Gold_Skulltula_024 and Gold_Skulltula_025 and Gold_Skulltula_026 and Gold_Skulltula_027 and Gold_Skulltula_028 and Gold_Skulltula_029 and Gold_Skulltula_030)')
    srule = srule.replace('(Gold_Skulltula_Token, 40)','(Gold_Skulltula_001 and Gold_Skulltula_002 and Gold_Skulltula_003 and Gold_Skulltula_004 and Gold_Skulltula_005 and Gold_Skulltula_006 and Gold_Skulltula_007 and Gold_Skulltula_008 and Gold_Skulltula_009 and Gold_Skulltula_010 and Gold_Skulltula_011 and Gold_Skulltula_012 and Gold_Skulltula_013 and Gold_Skulltula_014 and Gold_Skulltula_015 and Gold_Skulltula_016 and Gold_Skulltula_017 and Gold_Skulltula_018 and Gold_Skulltula_019 and Gold_Skulltula_020 and Gold_Skulltula_021 and Gold_Skulltula_022 and Gold_Skulltula_023 and Gold_Skulltula_024 and Gold_Skulltula_025 and Gold_Skulltula_026 and Gold_Skulltula_027 and Gold_Skulltula_028 and Gold_Skulltula_029 and Gold_Skulltula_030 and Gold_Skulltula_031 and Gold_Skulltula_032 and Gold_Skulltula_033 and Gold_Skulltula_034 and Gold_Skulltula_035 and Gold_Skulltula_036 and Gold_Skulltula_037 and Gold_Skulltula_038 and Gold_Skulltula_039 and Gold_Skulltula_040)')
    srule = srule.replace('(Gold_Skulltula_Token, 50)','(Gold_Skulltula_001 and Gold_Skulltula_002 and Gold_Skulltula_003 and Gold_Skulltula_004 and Gold_Skulltula_005 and Gold_Skulltula_006 and Gold_Skulltula_007 and Gold_Skulltula_008 and Gold_Skulltula_009 and Gold_Skulltula_010 and Gold_Skulltula_011 and Gold_Skulltula_012 and Gold_Skulltula_013 and Gold_Skulltula_014 and Gold_Skulltula_015 and Gold_Skulltula_016 and Gold_Skulltula_017 and Gold_Skulltula_018 and Gold_Skulltula_019 and Gold_Skulltula_020 and Gold_Skulltula_021 and Gold_Skulltula_022 and Gold_Skulltula_023 and Gold_Skulltula_024 and Gold_Skulltula_025 and Gold_Skulltula_026 and Gold_Skulltula_027 and Gold_Skulltula_028 and Gold_Skulltula_029 and Gold_Skulltula_030 and Gold_Skulltula_031 and Gold_Skulltula_032 and Gold_Skulltula_033 and Gold_Skulltula_034 and Gold_Skulltula_035 and Gold_Skulltula_036 and Gold_Skulltula_037 and Gold_Skulltula_038 and Gold_Skulltula_039 and Gold_Skulltula_040 and Gold_Skulltula_041 and Gold_Skulltula_042 and Gold_Skulltula_043 and Gold_Skulltula_044 and Gold_Skulltula_045 and Gold_Skulltula_046 and Gold_Skulltula_047 and Gold_Skulltula_048 and Gold_Skulltula_049 and Gold_Skulltula_050)')
    return srule

def testReplacements(itemArray, s, rule):
    for i in itemArray:
        if i == s('Deku_Sticks'):              r = 'OK'
        elif i == s('Deku_Nuts'):              r = 'OK'
        elif i == s('Bomb_Bag'):               r = 'OK'
        elif i == s('Bow'):                    r = 'OK'
        elif i == s('Fire_Arrows'):            r = 'OK'
        elif i == s('Dins_Fire'):              r = 'OK'
        elif i == s('Slingshot'):              r = 'OK'
        elif i == s('Ocarina'):                r = 'OK'
        elif i == s('Bombchus'):               r = 'OK'
        elif i == s('Hookshot'):               r = 'OK'
        elif i == s('Longshot'):               r = 'OK'
        elif i == s('Ice_Arrows'):             r = 'OK'
        elif i == s('Farores_Wind'):           r = 'OK'
        elif i == s('Boomerang'):              r = 'OK'
        elif i == s('Lens_of_Truth'):          r = 'OK'
        elif i == s('Magic_Beans'):            r = 'OK'
        elif i == s('Hammer'):                 r = 'OK'
        elif i == s('Light_Arrows'):           r = 'OK'
        elif i == s('Nayrus_Love'):            r = 'OK'
        elif i == s('Bottle'):                 r = 'OK'
        elif i == s('Bottle_with_Big_Poe1'):    r = 'OK'
        elif i == s('Bottle_with_Big_Poe2'):    r = 'OK'
        elif i == s('Bottle_with_Big_Poe3'):    r = 'OK'
        elif i == s('Bottle_with_Big_Poe4'):    r = 'OK'
        elif i == s('Bottle_with_Letter'):     r = 'OK'
        elif i == s('Adult_Trade_Item'):       r = 'OK'
        elif i == s('Child_Trade_Item'):       r = 'OK'
        elif i == s('Zeldas_Lullaby'):         r = 'OK'
        elif i == s('Eponas_Song'):            r = 'OK'
        elif i == s('Sarias_Song'):            r = 'OK'
        elif i == s('Suns_Song'):              r = 'OK'
        elif i == s('Song_of_Time'):           r = 'OK'
        elif i == s('Song_of_Storms'):         r = 'OK'
        elif i == s('Minuet'):                 r = 'OK'
        elif i == s('Bolero'):                 r = 'OK'
        elif i == s('Serenade'):               r = 'OK'
        elif i == s('Requiem'):                r = 'OK'
        elif i == s('Nocturne'):               r = 'OK'
        elif i == s('Prelude'):                r = 'OK'
        elif i == s('Scarecrow_Song'):         r = 'OK'
        elif i == s('Kokiri_Sword'):           r = 'OK'
        elif i == s('Master_Sword'):           r = 'OK'
        elif i == s('Biggoron_Sword'):         r = 'OK'
        elif i == s('Deku_Shield'):            r = 'OK'
        elif i == s('Hylian_Shield'):          r = 'OK'
        elif i == s('Mirror_Shield'):          r = 'OK'
        elif i == s('Bracelet'):               r = 'OK'
        elif i == s('Silver_Gauntlets'):       r = 'OK'
        elif i == s('Gold_Gauntlets'):         r = 'OK'
        elif i == s('Goron_Tunic'):            r = 'OK'
        elif i == s('Zora_Tunic'):             r = 'OK'
        elif i == s('Silver_Scale'):           r = 'OK'
        elif i == s('Gold_Scale'):             r = 'OK'
        elif i == s('Iron_Boots'):             r = 'OK'
        elif i == s('Hover_Boots'):            r = 'OK'
        elif i == s('Adult_Wallet'):           r = 'OK'
        elif i == s('Giant_Wallet'):           r = 'OK'
        elif i == s('Tycoon_Wallet'):          r = 'OK'
        elif i == s('Magic_Meter'):            r = 'OK'
        elif i == s('Gerudo_Membership'):      r = 'OK'
        elif i == s('Stone_of_Agony'):         r = 'OK'
        elif i == s('Fo_SK_1'):                r = 'OK'
        elif i == s('Fo_SK_2'):                r = 'OK'
        elif i == s('Fo_SK_3'):                r = 'OK'
        elif i == s('Fo_SK_4'):                r = 'OK'
        elif i == s('Fo_SK_5'):                r = 'OK'
        elif i == s('Fi_SK_1'):                r = 'OK'
        elif i == s('Fi_SK_2'):                r = 'OK'
        elif i == s('Fi_SK_3'):                r = 'OK'
        elif i == s('Fi_SK_4'):                r = 'OK'
        elif i == s('Fi_SK_5'):                r = 'OK'
        elif i == s('Fi_SK_6'):                r = 'OK'
        elif i == s('Fi_SK_7'):                r = 'OK'
        elif i == s('Fi_SK_8'):                r = 'OK'
        elif i == s('Wa_SK_1'):                r = 'OK'
        elif i == s('Wa_SK_2'):                r = 'OK'
        elif i == s('Wa_SK_3'):                r = 'OK'
        elif i == s('Wa_SK_4'):                r = 'OK'
        elif i == s('Wa_SK_5'):                r = 'OK'
        elif i == s('Wa_SK_6'):                r = 'OK'
        elif i == s('Sp_SK_1'):                r = 'OK'
        elif i == s('Sp_SK_2'):                r = 'OK'
        elif i == s('Sp_SK_3'):                r = 'OK'
        elif i == s('Sp_SK_4'):                r = 'OK'
        elif i == s('Sp_SK_5'):                r = 'OK'
        elif i == s('Sh_SK_1'):                r = 'OK'
        elif i == s('Sh_SK_2'):                r = 'OK'
        elif i == s('Sh_SK_3'):                r = 'OK'
        elif i == s('Sh_SK_4'):                r = 'OK'
        elif i == s('Sh_SK_5'):                r = 'OK'
        elif i == s('We_SK_1'):                r = 'OK'
        elif i == s('We_SK_2'):                r = 'OK'
        elif i == s('We_SK_3'):                r = 'OK'
        elif i == s('GF_SK_1'):                r = 'OK'
        elif i == s('GF_SK_2'):                r = 'OK'
        elif i == s('GF_SK_3'):                r = 'OK'
        elif i == s('GF_SK_4'):                r = 'OK'
        elif i == s('GTG_SK_1'):               r = 'OK'
        elif i == s('GTG_SK_2'):               r = 'OK'
        elif i == s('GTG_SK_3'):               r = 'OK'
        elif i == s('GTG_SK_4'):               r = 'OK'
        elif i == s('GTG_SK_5'):               r = 'OK'
        elif i == s('GTG_SK_6'):               r = 'OK'
        elif i == s('GTG_SK_7'):               r = 'OK'
        elif i == s('GTG_SK_8'):               r = 'OK'
        elif i == s('GTG_SK_9'):               r = 'OK'
        elif i == s('GC_SK_1'):                r = 'OK'
        elif i == s('GC_SK_2'):                r = 'OK'
        elif i == s('Fo_BK'):                  r = 'OK'
        elif i == s('Fi_BK'):                  r = 'OK'
        elif i == s('Wa_BK'):                  r = 'OK'
        elif i == s('Sp_BK'):                  r = 'OK'
        elif i == s('Sh_BK'):                  r = 'OK'
        elif i == s('GC_BK'):                  r = 'OK'
        elif i == s('Forest_Medallion'):       r = 'OK'
        elif i == s('Fire_Medallion'):         r = 'OK'
        elif i == s('Water_Medallion'):        r = 'OK'
        elif i == s('Spirit_Medallion'):       r = 'OK'
        elif i == s('Shadow_Medallion'):       r = 'OK'
        elif i == s('Light_Medallion'):        r = 'OK'
        elif i == s('Kokiri_Emerald'):         r = 'OK'
        elif i == s('Goron_Ruby'):             r = 'OK'
        elif i == s('Zora_Sapphire'):          r = 'OK'
        elif i == s('is_adult'):               r = 'OK'
        # new bits
        elif i == s('is_child'):                                r = 'OK'
        elif i == s('Gold_Skulltula_001'):                      r = 'OK'
        elif i == s('Gold_Skulltula_002'):                      r = 'OK'
        elif i == s('Gold_Skulltula_003'):                      r = 'OK'
        elif i == s('Gold_Skulltula_004'):                      r = 'OK'
        elif i == s('Gold_Skulltula_005'):                      r = 'OK'
        elif i == s('Gold_Skulltula_006'):                      r = 'OK'
        elif i == s('Gold_Skulltula_007'):                      r = 'OK'
        elif i == s('Gold_Skulltula_008'):                      r = 'OK'
        elif i == s('Gold_Skulltula_009'):                      r = 'OK'
        elif i == s('Gold_Skulltula_010'):                      r = 'OK'
        elif i == s('Gold_Skulltula_011'):                      r = 'OK'
        elif i == s('Gold_Skulltula_012'):                      r = 'OK'
        elif i == s('Gold_Skulltula_013'):                      r = 'OK'
        elif i == s('Gold_Skulltula_014'):                      r = 'OK'
        elif i == s('Gold_Skulltula_015'):                      r = 'OK'
        elif i == s('Gold_Skulltula_016'):                      r = 'OK'
        elif i == s('Gold_Skulltula_017'):                      r = 'OK'
        elif i == s('Gold_Skulltula_018'):                      r = 'OK'
        elif i == s('Gold_Skulltula_019'):                      r = 'OK'
        elif i == s('Gold_Skulltula_020'):                      r = 'OK'
        elif i == s('Gold_Skulltula_021'):                      r = 'OK'
        elif i == s('Gold_Skulltula_022'):                      r = 'OK'
        elif i == s('Gold_Skulltula_023'):                      r = 'OK'
        elif i == s('Gold_Skulltula_024'):                      r = 'OK'
        elif i == s('Gold_Skulltula_025'):                      r = 'OK'
        elif i == s('Gold_Skulltula_026'):                      r = 'OK'
        elif i == s('Gold_Skulltula_027'):                      r = 'OK'
        elif i == s('Gold_Skulltula_028'):                      r = 'OK'
        elif i == s('Gold_Skulltula_029'):                      r = 'OK'
        elif i == s('Gold_Skulltula_030'):                      r = 'OK'
        elif i == s('Gold_Skulltula_031'):                      r = 'OK'
        elif i == s('Gold_Skulltula_032'):                      r = 'OK'
        elif i == s('Gold_Skulltula_033'):                      r = 'OK'
        elif i == s('Gold_Skulltula_034'):                      r = 'OK'
        elif i == s('Gold_Skulltula_035'):                      r = 'OK'
        elif i == s('Gold_Skulltula_036'):                      r = 'OK'
        elif i == s('Gold_Skulltula_037'):                      r = 'OK'
        elif i == s('Gold_Skulltula_038'):                      r = 'OK'
        elif i == s('Gold_Skulltula_039'):                      r = 'OK'
        elif i == s('Gold_Skulltula_040'):                      r = 'OK'
        elif i == s('Gold_Skulltula_041'):                      r = 'OK'
        elif i == s('Gold_Skulltula_042'):                      r = 'OK'
        elif i == s('Gold_Skulltula_043'):                      r = 'OK'
        elif i == s('Gold_Skulltula_044'):                      r = 'OK'
        elif i == s('Gold_Skulltula_045'):                      r = 'OK'
        elif i == s('Gold_Skulltula_046'):                      r = 'OK'
        elif i == s('Gold_Skulltula_047'):                      r = 'OK'
        elif i == s('Gold_Skulltula_048'):                      r = 'OK'
        elif i == s('Gold_Skulltula_049'):                      r = 'OK'
        elif i == s('Gold_Skulltula_050'):                      r = 'OK'
        elif i == s('Gold_Skulltula_051'):                      r = 'OK'
        elif i == s('Gold_Skulltula_052'):                      r = 'OK'
        elif i == s('Gold_Skulltula_053'):                      r = 'OK'
        elif i == s('Gold_Skulltula_054'):                      r = 'OK'
        elif i == s('Gold_Skulltula_055'):                      r = 'OK'
        elif i == s('Gold_Skulltula_056'):                      r = 'OK'
        elif i == s('Gold_Skulltula_057'):                      r = 'OK'
        elif i == s('Gold_Skulltula_058'):                      r = 'OK'
        elif i == s('Gold_Skulltula_059'):                      r = 'OK'
        elif i == s('Gold_Skulltula_060'):                      r = 'OK'
        elif i == s('Gold_Skulltula_061'):                      r = 'OK'
        elif i == s('Gold_Skulltula_062'):                      r = 'OK'
        elif i == s('Gold_Skulltula_063'):                      r = 'OK'
        elif i == s('Gold_Skulltula_064'):                      r = 'OK'
        elif i == s('Gold_Skulltula_065'):                      r = 'OK'
        elif i == s('Gold_Skulltula_066'):                      r = 'OK'
        elif i == s('Gold_Skulltula_067'):                      r = 'OK'
        elif i == s('Gold_Skulltula_068'):                      r = 'OK'
        elif i == s('Gold_Skulltula_069'):                      r = 'OK'
        elif i == s('Gold_Skulltula_070'):                      r = 'OK'
        elif i == s('Gold_Skulltula_071'):                      r = 'OK'
        elif i == s('Gold_Skulltula_072'):                      r = 'OK'
        elif i == s('Gold_Skulltula_073'):                      r = 'OK'
        elif i == s('Gold_Skulltula_074'):                      r = 'OK'
        elif i == s('Gold_Skulltula_075'):                      r = 'OK'
        elif i == s('Gold_Skulltula_076'):                      r = 'OK'
        elif i == s('Gold_Skulltula_077'):                      r = 'OK'
        elif i == s('Gold_Skulltula_078'):                      r = 'OK'
        elif i == s('Gold_Skulltula_079'):                      r = 'OK'
        elif i == s('Gold_Skulltula_080'):                      r = 'OK'
        elif i == s('Gold_Skulltula_081'):                      r = 'OK'
        elif i == s('Gold_Skulltula_082'):                      r = 'OK'
        elif i == s('Gold_Skulltula_083'):                      r = 'OK'
        elif i == s('Gold_Skulltula_084'):                      r = 'OK'
        elif i == s('Gold_Skulltula_085'):                      r = 'OK'
        elif i == s('Gold_Skulltula_086'):                      r = 'OK'
        elif i == s('Gold_Skulltula_087'):                      r = 'OK'
        elif i == s('Gold_Skulltula_088'):                      r = 'OK'
        elif i == s('Gold_Skulltula_089'):                      r = 'OK'
        elif i == s('Gold_Skulltula_090'):                      r = 'OK'
        elif i == s('Gold_Skulltula_091'):                      r = 'OK'
        elif i == s('Gold_Skulltula_092'):                      r = 'OK'
        elif i == s('Gold_Skulltula_093'):                      r = 'OK'
        elif i == s('Gold_Skulltula_094'):                      r = 'OK'
        elif i == s('Gold_Skulltula_095'):                      r = 'OK'
        elif i == s('Gold_Skulltula_096'):                      r = 'OK'
        elif i == s('Gold_Skulltula_097'):                      r = 'OK'
        elif i == s('Gold_Skulltula_098'):                      r = 'OK'
        elif i == s('Gold_Skulltula_099'):                      r = 'OK'
        elif i == s('Gold_Skulltula_100'):                      r = 'OK'
        # world state
        elif i == s('Links_Cow_Obtained'):                      r = 'OK'
        elif i == s('Epona'):                                   r = 'OK'
        elif i == s('Water_Temple_Clear'):                      r = 'OK'
        # world logic
        elif i == s('lacs_vanilla'):                            r = 'OK'
        elif i == s('lacs_medallions'):                         r = 'OK'
        elif i == s('lacs_stones'):                             r = 'OK'
        elif i == s('lacs_ad'):                                 r = 'OK'
        elif i == s('scrubsanity'):                             r = 'OK'
        elif i == s('not_scrubsanity'):                         r = 'OK'
        elif i == s('chus_in_logic'):                           r = 'OK'
        elif i == s('big_poes1'):                               r = 'OK'
        elif i == s('big_poes2'):                               r = 'OK'
        elif i == s('big_poes3'):                               r = 'OK'
        elif i == s('big_poes4'):                               r = 'OK'
        elif i == s('big_poes5'):                               r = 'OK'
        elif i == s('big_poes6'):                               r = 'OK'
        elif i == s('big_poes7'):                               r = 'OK'
        elif i == s('big_poes8'):                               r = 'OK'
        elif i == s('big_poes9'):                               r = 'OK'
        elif i == s('big_poes10'):                              r = 'OK'
        elif i == s('logic_fewer_tunic_requirements'):          r = 'OK'
        elif i == s('logic_visible_collisions'):                r = 'OK'
        elif i == s('logic_child_deadhand'):                    r = 'OK'
        elif i == s('logic_child_dampe_race_poh'):              r = 'OK'
        elif i == s('logic_man_on_roof'):                       r = 'OK'
        elif i == s('logic_dc_staircase'):                      r = 'OK'
        elif i == s('logic_dc_jump'):                           r = 'OK'
        elif i == s('logic_gerudo_kitchen'):                    r = 'OK'
        elif i == s('logic_deku_basement_gs'):                  r = 'OK'
        elif i == s('logic_deku_b1_webs_with_bow'):             r = 'OK'
        elif i == s('logic_rusted_switches'):                   r = 'OK'
        elif i == s('logic_botw_basement'):                     r = 'OK'
        elif i == s('logic_forest_mq_block_puzzle'):            r = 'OK'
        elif i == s('logic_spirit_child_bombchu'):              r = 'OK'
        elif i == s('logic_windmill_poh'):                      r = 'OK'
        elif i == s('logic_crater_bean_poh_with_hovers'):       r = 'OK'
        elif i == s('logic_zora_with_cucco'):                   r = 'OK'
        elif i == s('logic_gtg_mq_with_hookshot'):              r = 'OK'
        elif i == s('logic_forest_vines'):                      r = 'OK'
        elif i == s('logic_forest_outdoor_east_gs'):            r = 'OK'
        elif i == s('logic_forest_well_swim'):                  r = 'OK'
        elif i == s('logic_forest_mq_hallway_switch'):          r = 'OK'
        elif i == s('logic_dmt_bombable'):                      r = 'OK'
        elif i == s('logic_water_bk_chest'):                    r = 'OK'
        elif i == s('logic_adult_kokiri_gs'):                   r = 'OK'
        elif i == s('logic_spirit_mq_frozen_eye'):              r = 'OK'
        elif i == s('logic_spirit_wall'):                       r = 'OK'
        elif i == s('logic_spirit_lobby_gs'):                   r = 'OK'
        elif i == s('logic_spirit_mq_sun_block_gs'):            r = 'OK'
        elif i == s('logic_jabu_scrub_jump_dive'):              r = 'OK'
        elif i == s('logic_jabu_mq_sot_gs'):                    r = 'OK'
        elif i == s('logic_botw_cage_gs'):                      r = 'OK'
        elif i == s('logic_botw_mq_dead_hand_key'):             r = 'OK'
        elif i == s('logic_fire_flame_maze'):                   r = 'OK'
        elif i == s('logic_fire_mq_flame_maze'):                r = 'OK'
        elif i == s('logic_fire_mq_climb'):                     r = 'OK'
        elif i == s('logic_fire_mq_near_boss'):                 r = 'OK'
        elif i == s('logic_fire_mq_maze_side_room'):            r = 'OK'
        elif i == s('logic_fire_mq_bk_chest'):                  r = 'OK'
        elif i == s('logic_zora_river_lower'):                  r = 'OK'
        elif i == s('logic_water_cracked_wall_hovers'):         r = 'OK'
        elif i == s('logic_shadow_freestanding_key'):           r = 'OK'
        elif i == s('logic_shadow_mq_huge_pit'):                r = 'OK'
        elif i == s('logic_mido_backflip'):                     r = 'OK'
        elif i == s('logic_fire_boss_door_jump'):               r = 'OK'
        elif i == s('logic_lab_diving'):                        r = 'OK'
        elif i == s('logic_biggoron_bolero'):                   r = 'OK'
        elif i == s('logic_wasteland_crossing'):                r = 'OK'
        elif i == s('logic_colossus_gs'):                       r = 'OK'
        elif i == s('logic_dc_scarecrow_gs'):                   r = 'OK'
        elif i == s('logic_kakariko_tower_gs'):                 r = 'OK'
        elif i == s('logic_lab_wall_gs'):                       r = 'OK'
        elif i == s('logic_spirit_mq_lower_adult'):             r = 'OK'
        elif i == s('logic_spirit_map_chest'):                  r = 'OK'
        elif i == s('logic_spirit_sun_chest'):                  r = 'OK'
        elif i == s('logic_shadow_trial_mq'):                   r = 'OK'
        elif i == s('logic_forest_outdoors_ledge'):             r = 'OK'
        elif i == s('logic_water_boss_key_region'):             r = 'OK'
        elif i == s('logic_water_falling_platform_gs'):         r = 'OK'
        elif i == s('logic_water_river_gs'):                    r = 'OK'
        elif i == s('logic_water_hookshot_entry'):              r = 'OK'
        elif i == s('logic_trail_gs_upper'):                    r = 'OK'
        elif i == s('logic_trail_gs_lower_hookshot'):           r = 'OK'
        elif i == s('logic_trail_gs_lower_bean'):               r = 'OK'
        elif i == s('logic_crater_upper_to_lower'):             r = 'OK'
        elif i == s('logic_zora_with_hovers'):                  r = 'OK'
        elif i == s('logic_shadow_statue'):                     r = 'OK'
        elif i == s('logic_link_goron_dins'):                   r = 'OK'
        elif i == s('logic_fire_song_of_time'):                 r = 'OK'
        elif i == s('logic_fire_strength'):                     r = 'OK'
        elif i == s('logic_fire_mq_bombable_chest'):            r = 'OK'
        elif i == s('logic_light_trial_mq'):                    r = 'OK'
        elif i == s('logic_ice_mq_scarecrow'):                  r = 'OK'
        elif i == s('logic_reverse_wasteland'):                 r = 'OK'
        elif i == s('logic_zora_river_upper'):                  r = 'OK'
        elif i == s('logic_shadow_mq_gap'):                     r = 'OK'
        elif i == s('logic_lost_woods_gs_bean'):                r = 'OK'
        elif i == s('logic_jabu_boss_gs_adult'):                r = 'OK'
        elif i == s('logic_graveyard_poh'):                     r = 'OK'
        elif i == s('logic_dmt_soil_gs'):                       r = 'OK'
        elif i == s('logic_gtg_without_hookshot'):              r = 'OK'
        elif i == s('logic_gtg_mq_without_hookshot'):           r = 'OK'
        elif i == s('logic_gtg_fake_wall'):                     r = 'OK'
        elif i == s('logic_water_cracked_wall_nothing'):        r = 'OK'
        elif i == s('logic_water_north_basement_ledge_jump'):   r = 'OK'
        elif i == s('logic_water_temple_torch_longshot'):       r = 'OK'
        elif i == s('logic_water_bk_jump_dive'):                r = 'OK'
        elif i == s('logic_water_dragon_jump_dive'):            r = 'OK'
        elif i == s('logic_water_dragon_bombchu'):              r = 'OK'
        elif i == s('logic_goron_city_leftmost'):               r = 'OK'
        elif i == s('logic_deku_b1_skip'):                      r = 'OK'
        elif i == s('logic_spirit_lower_adult_switch'):         r = 'OK'
        elif i == s('logic_forest_outside_backdoor'):           r = 'OK'
        elif i == s('logic_forest_scarecrow'):                  r = 'OK'
        elif i == s('logic_dc_mq_child_bombs'):                 r = 'OK'
        elif i == s('logic_dc_slingshot_skip'):                 r = 'OK'
        elif i == s('logic_child_rolling_with_strength'):       r = 'OK'
        elif i == s('logic_goron_city_pot'):                    r = 'OK'
        elif i == s('logic_valley_crate_hovers'):               r = 'OK'
        elif i == s('logic_lost_woods_bridge'):                 r = 'OK'
        elif i == s('logic_spirit_trial_hookshot'):             r = 'OK'
        elif i == s('logic_shadow_umbrella'):                   r = 'OK'
        elif i == s('logic_water_central_bow'):                 r = 'OK'
        elif i == s('logic_fire_scarecrow'):                    r = 'OK'
        elif i == s('logic_shadow_fire_arrow_entry'):           r = 'OK'
        else:
            print(rule)
            print('Unrecognized symbol: ' + str(i))

def compressItems(itemArray, tup, s):
    c = bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
    for i in itemArray:
        if i == s('Deku_Sticks') and tup[i]:            c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001')
        if i == s('Deku_Nuts') and tup[i]:              c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010')
        if i == s('Bomb_Bag') and tup[i]:               c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100')
        if i == s('Bow') and tup[i]:                    c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000')
        if i == s('Fire_Arrows') and tup[i]:            c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000')
        if i == s('Dins_Fire') and tup[i]:              c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000')
        if i == s('Slingshot') and tup[i]:              c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000')
        if i == s('Ocarina') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000')
        if i == s('Bombchus') and tup[i]:               c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000')
        if i == s('Hookshot') and tup[i]:               c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000')
        if i == s('Longshot') and tup[i]:               c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000')
        if i == s('Ice_Arrows') and tup[i]:             c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000')
        if i == s('Farores_Wind') and tup[i]:           c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000')
        if i == s('Boomerang') and tup[i]:              c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000')
        if i == s('Lens_of_Truth') and tup[i]:          c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000')
        if i == s('Magic_Beans') and tup[i]:            c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000')
        if i == s('Hammer') and tup[i]:                 c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000')
        if i == s('Light_Arrows') and tup[i]:           c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000')
        if i == s('Nayrus_Love') and tup[i]:            c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000')
        if i == s('Bottle') and tup[i]:                 c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000')
        if i == s('Bottle_with_Big_Poe') and tup[i]:    c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000')
        if i == s('Bottle_with_Letter') and tup[i]:     c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000')
        if i == s('Adult_Trade_Item') and tup[i]:       c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000')
        if i == s('Child_Trade_Item') and tup[i]:       c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000')
        if i == s('Zeldas_Lullaby') and tup[i]:         c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000')
        if i == s('Eponas_Song') and tup[i]:            c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000')
        if i == s('Sarias_Song') and tup[i]:            c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000')
        if i == s('Suns_Song') and tup[i]:              c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000')
        if i == s('Song_of_Time') and tup[i]:           c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000')
        if i == s('Song_of_Storms') and tup[i]:         c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000')
        if i == s('Minuet') and tup[i]:                 c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000')
        if i == s('Bolero') and tup[i]:                 c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000')
        if i == s('Serenade') and tup[i]:               c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000')
        if i == s('Requiem') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000')
        if i == s('Nocturne') and tup[i]:               c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000')
        if i == s('Prelude') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000')
        if i == s('Kokiri_Sword') and tup[i]:           c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000')
        if i == s('Master_Sword') and tup[i]:           c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000')
        if i == s('Biggoron_Sword') and tup[i]:         c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000')
        if i == s('Deku_Shield') and tup[i]:            c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000')
        if i == s('Hylian_Shield') and tup[i]:          c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000')
        if i == s('Mirror_Shield') and tup[i]:          c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000')
        if i == s('Bracelet') and tup[i]:               c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000')
        if i == s('Silver_Gauntlets') and tup[i]:       c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000')
        if i == s('Gold_Gauntlets') and tup[i]:         c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000')
        if i == s('Goron_Tunic') and tup[i]:            c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000')
        if i == s('Zora_Tunic') and tup[i]:             c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000')
        if i == s('Silver_Scale') and tup[i]:           c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000')
        if i == s('Gold_Scale') and tup[i]:             c = c | bitarray('00000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000')
        if i == s('Iron_Boots') and tup[i]:             c = c | bitarray('00000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000')
        if i == s('Hover_Boots') and tup[i]:            c = c | bitarray('00000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000')
        if i == s('Adult_Wallet') and tup[i]:           c = c | bitarray('00000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000')
        if i == s('Giant_Wallet') and tup[i]:           c = c | bitarray('00000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000')
        if i == s('Tycoon_Wallet') and tup[i]:          c = c | bitarray('00000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000')
        if i == s('Magic_Meter') and tup[i]:            c = c | bitarray('00000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000')
        if i == s('Gerudo_Membership') and tup[i]:      c = c | bitarray('00000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000')
        if i == s('Stone_of_Agony') and tup[i]:         c = c | bitarray('00000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000')
        if i == s('Fo_SK_1') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000')
        if i == s('Fo_SK_2') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000')
        if i == s('Fo_SK_3') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000')
        if i == s('Fo_SK_4') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000')
        if i == s('Fo_SK_5') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000')
        if i == s('Fi_SK_1') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000')
        if i == s('Fi_SK_2') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Fi_SK_3') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Fi_SK_4') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Fi_SK_5') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Fi_SK_6') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Fi_SK_7') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Fi_SK_8') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Wa_SK_1') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Wa_SK_2') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Wa_SK_3') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Wa_SK_4') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Wa_SK_5') and tup[i]:                c = c | bitarray('00000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Wa_SK_6') and tup[i]:                c = c | bitarray('00000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Sp_SK_1') and tup[i]:                c = c | bitarray('00000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Sp_SK_2') and tup[i]:                c = c | bitarray('00000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Sp_SK_3') and tup[i]:                c = c | bitarray('00000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Sp_SK_4') and tup[i]:                c = c | bitarray('00000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Sp_SK_5') and tup[i]:                c = c | bitarray('00000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Sh_SK_1') and tup[i]:                c = c | bitarray('00000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Sh_SK_2') and tup[i]:                c = c | bitarray('00000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Sh_SK_3') and tup[i]:                c = c | bitarray('00000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Sh_SK_4') and tup[i]:                c = c | bitarray('00000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Sh_SK_5') and tup[i]:                c = c | bitarray('00000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('We_SK_1') and tup[i]:                c = c | bitarray('00000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('We_SK_2') and tup[i]:                c = c | bitarray('00000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('We_SK_3') and tup[i]:                c = c | bitarray('00000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GF_SK_1') and tup[i]:                c = c | bitarray('00000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GF_SK_2') and tup[i]:                c = c | bitarray('00000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GF_SK_3') and tup[i]:                c = c | bitarray('00000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GF_SK_4') and tup[i]:                c = c | bitarray('00000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GTG_SK_1') and tup[i]:               c = c | bitarray('00000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GTG_SK_2') and tup[i]:               c = c | bitarray('00000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GTG_SK_3') and tup[i]:               c = c | bitarray('00000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GTG_SK_4') and tup[i]:               c = c | bitarray('00000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GTG_SK_5') and tup[i]:               c = c | bitarray('00000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GTG_SK_6') and tup[i]:               c = c | bitarray('00000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GTG_SK_7') and tup[i]:               c = c | bitarray('00000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GTG_SK_8') and tup[i]:               c = c | bitarray('00000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GTG_SK_9') and tup[i]:               c = c | bitarray('00000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GC_SK_1') and tup[i]:                c = c | bitarray('00000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GC_SK_2') and tup[i]:                c = c | bitarray('00000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Fo_BK') and tup[i]:                  c = c | bitarray('00000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Fi_BK') and tup[i]:                  c = c | bitarray('00001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Wa_BK') and tup[i]:                  c = c | bitarray('00010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Sp_BK') and tup[i]:                  c = c | bitarray('00100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Sh_BK') and tup[i]:                  c = c | bitarray('01000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('GC_BK') and tup[i]:                  c = c | bitarray('10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Forest_Medallion') and tup[i]:       c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Fire_Medallion') and tup[i]:         c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Water_Medallion') and tup[i]:        c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Spirit_Medallion') and tup[i]:       c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Shadow_Medallion') and tup[i]:       c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Light_Medallion') and tup[i]:        c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Kokiri_Emerald') and tup[i]:         c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Goron_Ruby') and tup[i]:             c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('Zora_Sapphire') and tup[i]:          c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        if i == s('is_adult') and tup[i]:               c = c | bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        # to do
        #if i == s('Gold_Skulltula') and tup[i]:         c = c | int('000000000000000000000000000000000000000000000000000000',2)
        #if i == s('World_Flag') and tup[i]:         c = c | int('000000000000000000000000000000000000000000000000000000',2)
    return c