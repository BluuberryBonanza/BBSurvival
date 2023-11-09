"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.utils.instances.bb_interaction_utils import BBInteractionUtils
from event_testing.results import TestResult
from event_testing.tests import TestList
from interactions import ParticipantType
from sims.sim_info_tests import SimInfoTest, MatchType

class _InteractionDisabler:
    interactions_disabled = False

    DISABLED_INTERACTION_IDS = [
        # Order a Delivery
        262154,  # phone_PickServices_Start_Deliveries
        261896,  # phone_pickServiceToHire_Deliveries
        269348,  # super_Pickservices_Start_Deliveries_FromFridge
        # Buy Gifts
        186241,  # purchase_HolidayTraditions_BuyGift_computer
        186367,  # purchase_HolidayTraditions_BuyGift_sim
        186369,  # purchase_HolidayTraditions_BuyGift_phone
        # Services
        9838,  # phone_pickServiceToHire
        262155,  # phone_PickServices_Start_Services
        329468,  # computer_HireService
        # Find a Job
        13223,  # computer_JoinCareer
        13787,  # phone_JoinCareer
        210156,  # phone_BrowseWebsites_OddJob_Find
        210160,  # computer_Browse_OddJob_Find
        # Call a FireFighter
        237652,  # phone_CallFirefighter
        239064,  # fire_CallFirefighter
        212088,  # sink_washHands_OffTheGrid
        212217,  # sink_BrushTeeth_OffTheGrid
        212246,  # shower_TakeShower_OffTheGrid
        # Purchase
        256727,  # purchasePickerInteraction_AnimalObjects_Chickens
        265795,  # purchasePickerInteraction_AnimalObjects_LivestockPen
        303830,  # purchasePickerInteraction_AnimalObjects_GoatSheep
        311069,  # purchasePickerInteraction_AnimalObjects_GoatSheep_FromPhone
        75892,  # Purchase_Books
        75897,  # Purchase_Upgrade_Parts
        75919,  # Purchase_Toys
        76322,  # Purchase_Seeds_Common
        76453,  # Purchase_Seeds_Uncommon
        77571,  # Purchase_Seeds_Common_computer
        77596,  # Purchase_Seeds_Uncommon_computer
        97544,  # Purchase_VoodooDoll
        99121,  # Purchase_Books_computer
        99422,  # Purchase_Toys_computer
        151914,  # purchase_Seeds_Vampire_Wolfsbane
        151930,  # purchase_Seeds_Vampire_Wolfsbane_Computer
        153843,  # purchase_Books_toddler
        188616,  # Purchase_Seeds_Rare
        188617,  # Purchase_Seeds_Rare_computer
        291578,  # purchase_Seeds_Vampire_Wolfsbane_Computer_VampireSecret
        310448,  # purchase_Upgrade_Parts_OnSim_Debug
        338357,  # phone_pickServiceToHire_Adoption_Horse_GoatSheep
        105670,  # purchase_Medicine
        155764,  # purchase_toys_HolidayCracker_computer
        271420,  # purchasePicker_FacialMask_Fridge
        271473,  # purchasePicker_FacialMask_Computer
        271544,  # facialMask_PurchaceAndApply_Child
        271594,  # purchasePicker_FacialMask_Fridge_PurchaseToApply
        273363,  # facialMask_PurchaseToApply_Start
        134051,  # object_Monsters_OrderBoostPack
        134329,  # object_Monsters_OrderBoostPack_5
        151376,  # purchase_VampireResearch_PlasmaPacks_Computer
        151913,  # purchase_Seeds_Vampire_Plasmafruit
        151915,  # purchase_Seeds_Vampire_SixamMosquitoTrap
        151925,  # purchase_Seeds_Vampire_Plasmafruit_Computer
        151933,  # purchase_Seeds_Vampire_SixamMosquitoTrap_Computer
        152951,  # purchase_VampireTomes_Vol1
        152952,  # purchase_VampireTomes_Vol1_Computer
        152954,  # purchase_VampireTomes_Vol2
        152955,  # purchase_VampireTomes_Vol2_Computer
        152958,  # purchase_VampireTomes_Vol3
        152959,  # purchase_VampireTomes_Vol3_Computer
        152961,  # purchase_VampireTomes_UltimateTome
        152962,  # purchase_VampireTomes_UltimateTome_Computer
        153962,  # purchase_Seeds_Vampire_Garlic
        153963,  # purchase_Seeds_Vampire_Garlic_computer
        177899,  # computer_PurchaseAntidote
        178019,  # mixer_social_CraftSalesTable_Purchase_ArchaeologyTable
        202178,  # purchase_ListeningDevice_Bugs
        235910,  # Purchase_Droid_Depot_Personality_Chips
        237404,  # purchase_Droid_Depot_Toys
        237407,  # batuu_Shells_Droid_Depot_Order_Toys
        239771,  # purchase_SNPC_Hondo_SmugglerGear
        239773,  # social_Batuu_SNPC_Hondo_PurchaseSmugglerGear
        242382,  # purchase_Holotable_FirstOrder
        242383,  # purchase_Holotable_Resistance
        244868,  # batuu_Shells_Droid_Depot_Order_Personality_Chips_Resistance
        244869,  # batuu_Shells_Droid_Depot_Order_Personality_Chips_FirstOrder
        244870,  # batuu_Shells_Droid_Depot_Order_Personality_Chips_Scoundrel
        244872,  # purchase_Droid_Depot_Personality_Chips_FirstOrder
        244873,  # purchase_Droid_Depot_Personality_Chips_Resistance
        244874,  # purchase_Droid_Depot_Personality_Chips_Scoundrel
        244883,  # holotable_UseToPurchase_FirstOrder
        244884,  # holotable_UseToPurchase_Resistance
        134937,  # purchase_FestivalFireworks_computer
        154889,  # purchase_FestivalFireworks_computer_child
        172834,  # vetVendingMachine_puchase_Player_NPC_owned
        172838,  # purchase_VetVendingMachine_generic
        172839,  # purchase_VetVendingMachine_owned
        172841,  # vetVendingMachine_puchase_Player_Player_owned
        176320,  # Purchase_PetToy
        181576,  # computer_SurpriseHoliday_PurchaseLotteryTicket
        181581,  # phone_SurpriseHoliday_PurchaseLotteryTicket
        185001,  # purchase_Seeds_Seasonal_Basic
        185002,  # purchase_Seeds_Seasonal_computer_Basic
        186241,  # purchase_HolidayTraditions_BuyGift_computer
        186367,  # purchase_HolidayTraditions_BuyGift_sim
        186369,  # purchase_HolidayTraditions_BuyGift_phone
        190715,  # purchase_Seeds_Seasonal_Plus
        190716,  # purchase_Seeds_Seasonal_computer_Plus
        194620,  # purchase_Crystals_All
        232916,  # Purchase_Dyes_computer
        239864,  # purchase_Seeds_VerticalGarden
        239912,  # purchase_CandleMakingStation_PurchaseDyeAndWax
        248495,  # vendingMachine_PurchaseConsumableHunger_HotFoodAndDrink
        248712,  # vendingMachine_Interactions_PurchaseConsumableCoffee_HotFoodAndDrink
        248713,  # vendingMachine_Interactions_PurchaseConsumableTea_HotFoodAndDrink
        248715,  # vendingMachine_Interactions_PurchaseConsumableHungerFood_ColdDrinkAndSnack
        248716,  # vendingMachine_Interactions_PurchaseConsumableCoffee_ColdDrinkAndSnack
        248717,  # vendingMachine_Interactions_PurchaseConsumableTea_ColdDrinkAndSnack
        248719,  # vendingMachine_Interactions_PurchaseConsumableHungerFruit_ColdDrinkAndSnack
        249093,  # vendingMachine_Interactions_PurchaseAndWearCAS_Yukata
        249124,  # vendingMachine_Interactions_PurchaseCAS_Yukata
        249393,  # vendingMachine_Interactions_Browse_PurchaseItem_ColdDrinkAndSnack
        249394,  # vendingMachine_Interactions_Browse_PurchaseItem_HotFoodAndDrink
        249484,  # vendingMachine_Interactions_PurchaseCAS_PaperHat
        249486,  # vendingMachine_Interactions_PurchaseAndWearCAS_PaperHat
        249871,  # vendingMachine_Interactions_Browse_PurchaseCapsule
        249872,  # vendingMachine_Interactions_PurchaseCapsule
        250298,  # vendingMachine_Interactions_PurchaseAndWearCAS_SnowOutfit
        250299,  # vendingMachine_Interactions_PurchaseCAS_SnowOutfit
        252361,  # purchase_WildlifeEncounter_AdventureGear
        252402,  # computer_RockClimbingGear_Purchase
        182223,  # Purchase_Rodent_Cure_computer
        183356,  # pet_Minor_Cage_Immediate_Purchase_Rodent
        185105,  # purchase_Rodent_Cure_Phone
        185633,  # purchase_Rodent_Treats_computer
        256727,  # purchasePickerInteraction_AnimalObjects_Chickens
        261619,  # super_GiantCrops_Plant_PurchaseSeeds_Computer
        261620,  # super_GiantCrops_Plant_PurchaseSeeds_Patch
        265795,  # purchasePickerInteraction_AnimalObjects_LivestockPen
        270410,  # super_GiantCrops_Plant_PurchaseFertilizer_Patch
        289889,  # vendingMachine_Interactions_Browse_PurchaseItem_HighSchool
        303830,  # purchasePickerInteraction_AnimalObjects_GoatSheep
        311069,  # purchasePickerInteraction_AnimalObjects_GoatSheep_FromPhone
        324112,  # computer_HorseTransaction_BuyHorse
        324115,  # phone_HorseTransaction_BuyHorse
        324815,  # buy_Horse_Computer
        324818,  # buy_Horse_Phone
        324821,  # buy_Horse_Shell
        328966,  # buyPickedHorse_PhoneComputer
        330568,  # buyPickedHorse_Shell
        331039,  # buy_Horse_Phone_HorseBed
        331040,  # buyPickedHorse_PhoneComputer_HorseBed
        337879,  # immediate_HorseTransaction_Phone_BuyHorse_HorseBed
        340351,  # purchase_RanchNectarMaker_Ingredients
        343183,  # buyPickedHorse_PhoneComputer_Apartment
        343673,  # buyPickedHorse_PhoneComputer_HorseBed_Apartment
        281478,  # purchase_WeddingCake_Computer
        281479,  # purchase_WeddingCake_Sim
        281579,  # mixer_Social_PurchaseWeddingCake
        286725,  # marketStalls_ShopFor_WeddingCake_Patisserie
        286727,  # purchase_MarketStalls_Wedding_Cake
        109634,  # retail_BuyItemFromInventory
        107746,  # mannequin_OutfitChange_BuyOutfit_AllowClobber
        107707,  # mannequin_RemoveOutfit_Picker_Swimwear
        107706,  # mannequin_RemoveOutfit_Picker_Party
        107705,  # mannequin_RemoveOutfit_Picker_Sleep
        107704,  # mannequin_RemoveOutfit_Picker_Athletic
        107703,  # mannequin_RemoveOutfit_Picker_Formal
        107702,  # mannequin_RemoveOutfit_Picker_Everyday
        269939,  # purchase_MarketStalls_MusicFestival
        324408,  # sI_AnimalFeederInteractions_RefillFeed

        # Maybe remove later?
        116619,  # si_Retail_BuyItemFromInventory_Autonomous
        145263,  # si_CraftSalesTable_PurchaseObject_Autonomous
        145262,  # si_CraftSalesTable_PurchaseObject
        233486,  # trashUpdate_GoToGarbageDump
        233487,  # virtualRabbitHoleInteractions_trashUpdate
        231894,  # Empty_Trash_Outdoor_TrashUpdate
        231893,  # trashUpdate_Collect_NoTargetRecyclables
        254791,  # collect_Trash_Compost_Aggregate
        331478,  # interactionPickerSI_CommunityBoard_Jobs
    ]


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbs_disable_interactions_on_zone_load(event: BBOnZoneLoadEndEvent):
    if _InteractionDisabler.interactions_disabled:
        return
    _InteractionDisabler.interactions_disabled = True

    for interaction_id in _InteractionDisabler.DISABLED_INTERACTION_IDS:
        interaction = BBInteractionUtils.load_interaction_by_guid(interaction_id)
        if interaction is None:
            continue
        impossible_sim_info_test = SimInfoTest()
        impossible_sim_info_test.who = ParticipantType.Actor
        impossible_sim_info_test.gender = None
        impossible_sim_info_test.ages = (0,)
        impossible_sim_info_test.species = None
        impossible_sim_info_test.can_age_up = None
        impossible_sim_info_test.npc = False
        impossible_sim_info_test.has_been_played = False
        impossible_sim_info_test.is_active_sim = True
        impossible_sim_info_test.match_type = MatchType.MATCH_ALL
        interaction.test_globals = TestList((impossible_sim_info_test,))
    return TestResult.TRUE
