import ui
import player
import mouseModule
import net
import app
import snd
import item
import player
import chat
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder
import localeInfo
import constInfo
import ime
import wndMgr
import dbg

if app.ENABLE_CHEQUE_SYSTEM:
	import uiToolTip
	import uiPickETC

if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import acce
from _weakref import proxy

ITEM_MALL_BUTTON_ENABLE = True

ITEM_FLAG_APPLICABLE = 1 << 14

class CostumeWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception

		if not app.ENABLE_COSTUME_SYSTEM:
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	@ui.WindowDestroy
	def Destroy(self):
		self.ClearDictionary()
		self.wndInventory = None

	def Show(self):
		self.__LoadWindow()
		self.RefreshCostumeSlot()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/CostumeWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("CostumeSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndEquip = wndEquip

	def RefreshCostumeSlot(self):
		getItemVNum=player.GetItemIndex

		for i in xrange(item.COSTUME_SLOT_COUNT):
			slotNumber = item.COSTUME_SLOT_START + i
			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)

		if app.ENABLE_WEAPON_COSTUME_SYSTEM:
			self.wndEquip.SetItemSlot(item.COSTUME_SLOT_WEAPON, getItemVNum(item.COSTUME_SLOT_WEAPON), 0)

		self.wndEquip.RefreshSlot()

class BeltInventoryWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception

		if not app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory

		self.wndBeltInventoryLayer = None
		self.wndBeltInventorySlot = None
		self.expandBtn = None
		self.minBtn = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	@ui.WindowDestroy
	def Destroy(self):
		self.wndInventory = None

	def Show(self, openBeltSlot = False):
		self.__LoadWindow()
		self.RefreshSlot()

		ui.ScriptWindow.Show(self)

		if openBeltSlot:
			self.OpenInventory()
		else:
			self.CloseInventory()

		self.SetTop()

	def Close(self):
		self.Hide()

	def IsOpeningInventory(self):
		if self.wndBeltInventoryLayer:
			return self.wndBeltInventoryLayer.IsShow()
		return False

	def OpenInventory(self):
		self.wndBeltInventoryLayer.Show()
		self.expandBtn.Hide()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()

	def CloseInventory(self):
		self.wndBeltInventoryLayer.Hide()
		self.expandBtn.Show()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()

	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()
		return x - 148, y + 241

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()

		if self.IsOpeningInventory():
			self.SetPosition(bx, by)
			self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())

		else:
			self.SetPosition(bx + 138, by);
			self.SetSize(10, self.GetHeight())

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/BeltInventoryWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			self.ORIGINAL_WIDTH = self.GetWidth()
			wndBeltInventorySlot = self.GetChild("BeltInventorySlot")
			self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
			self.expandBtn = self.GetChild("ExpandBtn")
			self.minBtn = self.GetChild("MinimizeBtn")

			self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
			self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))

			if localeInfo.IsARABIC() :
				self.expandBtn.SetPosition(self.expandBtn.GetWidth() - 2, 15)
				self.wndBeltInventoryLayer.SetPosition(self.wndBeltInventoryLayer.GetWidth() - 5, 0)
				self.minBtn.SetPosition(self.minBtn.GetWidth() + 3, 15)

			for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
				slotNumber = item.BELT_INVENTORY_SLOT_START + i
				wndBeltInventorySlot.SetCoverButton(slotNumber,	"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", False, False)

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndBeltInventorySlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndBeltInventorySlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndBeltInventorySlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndBeltInventorySlot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndBeltInventorySlot = wndBeltInventorySlot

	def RefreshSlot(self):
		getItemVNum=player.GetItemIndex

		for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
			slotNumber = item.BELT_INVENTORY_SLOT_START + i
			self.wndBeltInventorySlot.SetItemSlot(slotNumber, getItemVNum(slotNumber), player.GetItemCount(slotNumber))
			self.wndBeltInventorySlot.SetAlwaysRenderCoverButton(slotNumber, True)

			avail = "0"

			if player.IsAvailableBeltInventoryCell(slotNumber):
				self.wndBeltInventorySlot.EnableCoverButton(slotNumber)
			else:
				self.wndBeltInventorySlot.DisableCoverButton(slotNumber)

		self.wndBeltInventorySlot.RefreshSlot()


class InventoryWindow(ui.ScriptWindow):

	USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE", "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET")
	if app.ENABLE_USE_COSTUME_ATTR:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_CHANGE_COSTUME_ATTR", "USE_RESET_COSTUME_ATTR"])

	questionDialog = None
	tooltipItem = None
	wndCostume = None
	wndBelt = None
	dlgPickMoney = None
	if app.ENABLE_CHEQUE_SYSTEM:
		dlgPickETC = None

	interface = None

	sellingSlotNumber = -1
	isLoaded = 0
	isOpenedCostumeWindowWhenClosingInventory = 0
	isOpenedBeltWindowWhenClosingInventory = 0

	if app.ENABLE_GROWTH_PET_SYSTEM:
		petHatchingWindow	= None
		petFeedWindow		= None
		petNameChangeWindow = None

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isOpenedBeltWindowWhenClosingInventory = 0

		self.inventoryPageIndex = 0

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcceCombine = None
			self.wndAcceAbsorption = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

		self.RefreshItemSlot()
		self.RefreshStatus()

		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show()

		if self.wndBelt:
			self.wndBelt.Show(self.isOpenedBeltWindowWhenClosingInventory)

	def BindInterfaceClass(self, interface):
		self.interface = interface
		if app.ENABLE_WON_EXCHANGE_WINDOW and self.interface and self.wndChequeSlot:
			self.wndChequeSlot.SetEvent(ui.__mem_func__(self.interface.ToggleWonExchangeWindow))

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				if not localeInfo.IsARABIC():
					pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindowEx.py")
				else:
					pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "InventoryWindow.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindow.py")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.wndMoney = self.GetChild("Money")
			self.wndMoneySlot = self.GetChild("Money_Slot")
			self.mallButton = self.GetChild2("MallButton")
			self.DSSButton = self.GetChild2("DSSButton")
			self.costumeButton = self.GetChild2("CostumeButton")

			if app.ENABLE_CHEQUE_SYSTEM:
				self.wndCheque = self.GetChild("Cheque")
				self.wndChequeSlot = self.GetChild("Cheque_Slot")

				self.wndMoneyIcon = self.GetChild("Money_Icon")
				self.wndChequeIcon = self.GetChild("Cheque_Icon")

				self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 0)
				self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 1)

				self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 0)
				self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 1)

				self.toolTip = uiToolTip.ToolTip()
				self.toolTip.ClearToolTip()


			self.inventoryTab = []
			for i in xrange(player.INVENTORY_PAGE_COUNT):
				self.inventoryTab.append(self.GetChild("Inventory_Tab_%02d" % (i+1)))

			self.equipmentTab = []
			self.equipmentTab.append(self.GetChild("Equipment_Tab_01"))
			self.equipmentTab.append(self.GetChild("Equipment_Tab_02"))

			if self.costumeButton and not app.ENABLE_COSTUME_SYSTEM:
				self.costumeButton.Hide()
				self.costumeButton.Destroy()
				self.costumeButton = 0

			# Belt Inventory Window
			self.wndBelt = None

			if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
				self.wndBelt = BeltInventoryWindow(self)

			self.dlgQuestion = uiCommon.QuestionDialog2()
			self.dlgQuestion.Close()

			if app.ENABLE_GROWTH_PET_SYSTEM:
				self.PetItemQuestionDlg = uiCommon.QuestionDialog()
				self.PetItemQuestionDlg.Close()

				self.PetSkillDelDlg = uiCommon.QuestionDialog2()
				self.PetSkillDelDlg.Close()
				self.PetSkillAllDelBookIndex = -1

		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

		## Item
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## Equipment
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.Hide()

		## PickETCDialog
		if app.ENABLE_CHEQUE_SYSTEM:
			dlgPickETC = uiPickETC.PickETCDialog()
			dlgPickETC.LoadDialog()
			dlgPickETC.Hide()

		## RefineDialog
		self.refineDialog = uiRefine.RefineDialog()
		self.refineDialog.Hide()

		## AttachMetinDialog
		self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
		self.attachMetinDialog.Hide()

		## MoneySlot
		if app.ENABLE_CHEQUE_SYSTEM:
			self.wndChequeSlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 1)
			self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 0)
		else:
			self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		for i in xrange(player.INVENTORY_PAGE_COUNT):
			self.inventoryTab[i].SAFE_SetEvent(self.SetInventoryPage, i)
		self.inventoryTab[0].Down()

		self.equipmentTab[0].SAFE_SetEvent(self.SetEquipmentPage, 0)
		self.equipmentTab[1].SAFE_SetEvent(self.SetEquipmentPage, 1)
		self.equipmentTab[0].Down()
		self.equipmentTab[0].Hide()
		self.equipmentTab[1].Hide()

		self.wndItem = wndItem
		self.wndEquip = wndEquip
		self.dlgPickMoney = dlgPickMoney

		if app.ENABLE_CHEQUE_SYSTEM:
			self.dlgPickETC = dlgPickETC

		# MallButton
		if self.mallButton:
			self.mallButton.SetEvent(ui.__mem_func__(self.ClickMallButton))

		if self.DSSButton:
			self.DSSButton.SetEvent(ui.__mem_func__(self.ClickDSSButton))

		# Costume Button
		if self.costumeButton:
			self.costumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))

		self.wndCostume = None

 		#####
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.listAttachedAcces = []

		## Refresh
		self.SetInventoryPage(0)
		self.SetEquipmentPage(0)
		self.RefreshItemSlot()
		self.RefreshStatus()

	@ui.WindowDestroy
	def Destroy(self):
		self.ClearDictionary()

		if self.dlgPickMoney:
			self.dlgPickMoney.Destroy()
			self.dlgPickMoney = 0

		if self.refineDialog:
			self.refineDialog.Destroy()
			self.refineDialog = 0

		if app.ENABLE_CHEQUE_SYSTEM and self.dlgPickETC:
			self.dlgPickETC.Destroy()
			self.dlgPickETC = 0

		if self.attachMetinDialog:
			self.attachMetinDialog.Destroy()
			self.attachMetinDialog = 0

		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.dlgPickMoney = 0
		self.wndMoney = 0
		self.wndMoneySlot = 0
		if app.ENABLE_CHEQUE_SYSTEM:
			self.wndCheque = 0
			self.wndChequeSlot = 0
			self.dlgPickETC = 0
		self.questionDialog = None
		self.mallButton = None
		self.DSSButton = None
		self.costumeButton = None
		self.wndDragonSoulRefine = None
		self.interface = None

		if self.wndCostume:
			self.wndCostume.Destroy()
			self.wndCostume = None

		if self.wndBelt:
			self.wndBelt.Destroy()
			self.wndBelt = None

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcceCombine = None
			self.wndAcceAbsorption = None

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.petHatchingWindow:
				self.petHatchingWindow = None

			if self.petFeedWindow:
				self.petFeedWindow = None

			if self.petNameChangeWindow:
				self.petNameChangeWindow = None 

		self.inventoryTab = []
		self.equipmentTab = []

	def Hide(self):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()
			self.wndCostume.Close()

		if self.wndBelt:
			self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()
			print "Is Opening Belt Inven?? ", self.isOpenedBeltWindowWhenClosingInventory
			self.wndBelt.Close()

		if self.dlgPickMoney:
			self.dlgPickMoney.Close()

		if app.ENABLE_CHEQUE_SYSTEM:
			if self.dlgPickETC:
				self.dlgPickETC.Close()

		wndMgr.Hide(self.hWnd)


	def Close(self):
		self.Hide()

	def SetInventoryPage(self, page):
		self.inventoryPageIndex = page
		for i in xrange(player.INVENTORY_PAGE_COUNT):
			if i!=page:
				self.inventoryTab[i].SetUp()
		self.RefreshBagSlotWindow()

	def SetEquipmentPage(self, page):
		self.equipmentPageIndex = page
		self.equipmentTab[1-page].SetUp()
		self.RefreshEquipSlotWindow()

	def ClickMallButton(self):
		print "click_mall_button"
		net.SendChatPacket("/click_mall")

	# DSSButton
	def ClickDSSButton(self):
		print "click_dss_button"
		self.interface.ToggleDragonSoulWindow()

	def ClickCostumeButton(self):
		print "Click Costume Button"
		if self.wndCostume:
			if self.wndCostume.IsShow():
				self.wndCostume.Hide()
			else:
				self.wndCostume.Show()
		else:
			self.wndCostume = CostumeWindow(self)
			self.wndCostume.Show()

	def OpenPickMoneyDialog(self, focus_idx = 0):
		if mouseModule.mouseController.isAttached():
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_SAFEBOX == mouseModule.mouseController.GetAttachedType():
				if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

			mouseModule.mouseController.DeattachObject()

		else:
			curMoney = player.GetElk()
			if app.ENABLE_CHEQUE_SYSTEM:
				curCheque = player.GetCheque()
				if curMoney <= 0 and curCheque <= 0:
					return
			else:
				curCheque = 1 # default money value
				if curMoney <= 0:
					return

			self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
			self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
			self.dlgPickMoney.Open(curMoney, curCheque)
			if app.ENABLE_CHEQUE_SYSTEM:
				if focus_idx==0:
					self.dlgPickMoney.SetMaxCheque(3)
					self.dlgPickMoney.SetMax(9)
				else:
					self.dlgPickMoney.SetMax(9)
					self.dlgPickMoney.SetMaxCheque(3)
				self.dlgPickMoney.SetFocus(focus_idx)
			else:
				self.dlgPickMoney.SetMax(9)

	def OnPickMoney(self, money, cheque=0):
		mouseModule.mouseController.AttachMoney(self, player.SLOT_TYPE_INVENTORY, money, cheque)

	def OnPickItem(self, count):
		if app.ENABLE_CHEQUE_SYSTEM:
			itemSlotIndex = self.dlgPickETC.itemGlobalSlotIndex
		else:
			itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex
		selectedItemVNum = player.GetItemIndex(itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
			return local

		return self.inventoryPageIndex*player.INVENTORY_PAGE_SIZE + local

	if app.WJ_ENABLE_TRADABLE_ICON:
		def GetInventoryPageIndex(self):
			return self.inventoryPageIndex

	def RefreshBagSlotWindow(self):
		if app.WJ_ENABLE_TRADABLE_ICON:
			if not self.wndItem:
				return

		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot

		if app.WJ_ENABLE_TRADABLE_ICON:
			if self.interface:
				onTopWindow = self.interface.GetOnTopWindow()

		for i in xrange(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(slotNumber)
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			itemVnum = getItemVNum(slotNumber)
			setItemVNum(i, itemVnum, itemCount)

			if app.ENABLE_GROWTH_PET_SYSTEM:
				if constInfo.IS_PET_ITEM(itemVnum):
					self.__ActivePetHighlightSlot(slotNumber)
					self.__SetCoolTimePetItemSlot(slotNumber, itemVnum)

			if constInfo.IS_AUTO_POTION(itemVnum):
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]

				isActivated = 0 != metinSocket[0]

				if isActivated:
					self.wndItem.ActivateSlot(i)
					potionType = 0
					if constInfo.IS_AUTO_POTION_HP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_HP
					elif constInfo.IS_AUTO_POTION_SP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_SP

					usedAmount = int(metinSocket[1])
					totalAmount = int(metinSocket[2])
					player.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))

				else:
					self.wndItem.DeactivateSlot(i)

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				slotNumberChecked = 0

				for j in xrange(acce.WINDOW_MAX_MATERIALS):
					(isHere, iCell) = acce.GetAttachedItem(j)
					if isHere:
						if iCell == slotNumber:
							self.wndItem.ActivateSlot(i, (36.00 / 255.0), (222.00 / 255.0), (3.00 / 255.0), 1.0)
							if not slotNumber in self.listAttachedAcces:
								self.listAttachedAcces.append(slotNumber)

							slotNumberChecked = 1
					else:
						if slotNumber in self.listAttachedAcces and not slotNumberChecked:
							self.wndItem.DeactivateSlot(i)
							self.listAttachedAcces.remove(slotNumber)

			if item.ITEM_TYPE_PET == item.GetItemType() and item.PET_PAY == item.GetItemSubType():
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
				isActivated = 0 != metinSocket[2]
				if isActivated:
					self.wndItem.ActivateSlot(i)
				else:
					self.wndItem.DeactivateSlot(i)

			if app.WJ_ENABLE_TRADABLE_ICON:
				if itemVnum and self.interface and onTopWindow:
					if self.interface.MarkUnusableInvenSlotOnTopWnd(onTopWindow, slotNumber):
						if itemVnum == 50200:
							self.wndItem.SetCantMouseEventSlot(i)
						else:
							self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

		self.wndItem.RefreshSlot()

		if self.wndBelt:
			self.wndBelt.RefreshSlot()

	def SetItemSlotVnum(self, slotNumber):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndEquip.SetItemSlot
		itemCount = getItemCount(slotNumber)
		if itemCount <= 1:
			itemCount = 0
		setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)
		return

	def RefreshEquipSlotWindow(self):
		SetItemSlotVnum = self.SetItemSlotVnum
		for i in xrange(player.EQUIPMENT_PAGE_COUNT):
			SetItemSlotVnum(player.EQUIPMENT_SLOT_START + i)

		if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			SetItemSlotVnum(item.EQUIPMENT_BELT)
		if app.ENABLE_PENDANT_SYSTEM:
			SetItemSlotVnum(item.EQUIPMENT_PENDANT)
		if app.ENABLE_GLOVE_SYSTEM:
			SetItemSlotVnum(item.EQUIPMENT_GLOVE)

		self.wndEquip.RefreshSlot()

		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def RefreshStatus(self):
		money = player.GetElk()
		self.wndMoney.SetText(localeInfo.NumberToString(money) if app.ENABLE_CHEQUE_SYSTEM else localeInfo.NumberToMoneyString(money))
		if app.ENABLE_CHEQUE_SYSTEM:
			cheque = player.GetCheque()
			self.wndCheque.SetText(localeInfo.NumberToGoldNotText(cheque))

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SellItem(self):
		if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
			if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
				net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)
				snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return

		#net.SendItemUseToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				#@fixme011 BEGIN (block ds equip)
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					mouseModule.mouseController.DeattachObject()
					return
				#@fixme011 END

				itemCount = player.GetItemCount(attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)

			elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:

				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)

			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				#@fixme011 BEGIN (block ds equip)
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					mouseModule.mouseController.DeattachObject()
					return
				#@fixme011 END
				self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()

		else:

			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)

			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = player.GetItemCount(itemSlotIndex)

				if app.ENABLE_CHEQUE_SYSTEM:
					if itemCount > 1:
						self.dlgPickETC.SetTitleName(localeInfo.PICK_ITEM_TITLE)
						self.dlgPickETC.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
						self.dlgPickETC.Open(itemCount)
						self.dlgPickETC.itemGlobalSlotIndex = itemSlotIndex
				else:
					if itemCount > 1:
						self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
						self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
						self.dlgPickMoney.Open(itemCount)
						self.dlgPickMoney.itemGlobalSlotIndex = itemSlotIndex
				#else:
					#selectedItemVNum = player.GetItemIndex(itemSlotIndex)
					#mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum)

			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)

				if True == item.CanAddToQuickSlotItem(itemIndex):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)

			else:
				selectedItemVNum = player.GetItemIndex(itemSlotIndex)
				itemCount = player.GetItemCount(itemSlotIndex)

				if app.ENABLE_GROWTH_PET_SYSTEM:
					if self.__CanAttachGrowthPetItem(selectedItemVNum, itemSlotIndex):
						mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
				else:
					mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)

				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
					self.wndItem.SetUseMode(True)
				else:
					self.wndItem.SetUseMode(False)

				snd.PlaySound("sound/ui/pick.wav")

	if app.ENABLE_CHEQUE_SYSTEM:
		def OverInToolTip(self, arg):
			arglen = len(str(arg))
			pos_x, pos_y = wndMgr.GetMousePosition()

			self.toolTip.ClearToolTip()
			self.toolTip.SetThinBoardSize(11 * arglen)
			self.toolTip.SetToolTipPosition(pos_x + 5, pos_y - 5)
			self.toolTip.AppendTextLine(arg, 0xffffff00)
			self.toolTip.Show()

		def OverOutToolTip(self):
			self.toolTip.Hide()

		def EventProgress(self, event_type, idx):
			if "mouse_over_in" == str(event_type):
				if idx == 0 :
					self.OverInToolTip(localeInfo.CHEQUE_SYSTEM_UNIT_YANG)
				elif idx == 1 :
					self.OverInToolTip(localeInfo.CHEQUE_SYSTEM_UNIT_WON)
				else:
					return
			elif "mouse_over_out" == str(event_type) :
				self.OverOutToolTip()
			else:
				return

	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
		if srcItemSlotPos == dstItemSlotPos:
			return

		# cyh itemseal 2013 11 08
		if app.ENABLE_SOULBIND_SYSTEM and item.IsSealScroll(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.IsRefineScroll(srcItemVID):
			if constInfo.ENABLE_SELF_STACK_SCROLLS and player.GetItemIndex(srcItemSlotPos) == player.GetItemIndex(dstItemSlotPos):
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos,0)
			else:
				self.RefineItem(srcItemSlotPos, dstItemSlotPos)
				self.wndItem.SetUseMode(False)

		elif item.IsMetin(srcItemVID):
			self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif constInfo.ENABLE_SELF_STACK_SCROLLS and srcItemVID in (71052,71051,71084,71085):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		else:
			#snd.PlaySound("sound/ui/drop.wav")

			if app.ENABLE_GROWTH_PET_SYSTEM:
				if self.__IsPetItem(srcItemVID):
					if self.__SendUsePetItemToItemPacket(srcItemVID, srcItemSlotPos, dstItemSlotPos):
						return

			if player.IsEquipmentSlot(dstItemSlotPos):

				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)

			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
				#net.SendItemMovePacket(srcItemSlotPos, dstItemSlotPos, 0)

	def __SellItem(self, itemSlotPos):
		if not player.IsEquipmentSlot(itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(itemSlotPos)
			itemCount = player.GetItemCount(itemSlotPos)


			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			## 20140220
			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return

			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				itemPrice = itemCount / itemPrice
			else:
				itemPrice = itemPrice * itemCount

			if not app.ENABLE_NO_SELL_PRICE_DIVIDED_BY_5:
				itemPrice /= 5

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def __OnClosePopupDialog(self):
		self.pop = None

	def RefineItem(self, scrollSlotPos, targetSlotPos):

		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
			return

		###########################################################
		self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)
		#net.SendItemUseToItemPacket(scrollSlotPos, targetSlotPos)
		return

	def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if not player.CanDetach(scrollIndex, targetSlotPos):
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == acce.CLEAN_ATTR_VALUE0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ACCE_FAILURE_CLEAN)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
			return

		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			item.SelectItem(targetIndex)
			if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == acce.CLEAN_ATTR_VALUE0:
					self.questionDialog.SetText(localeInfo.ACCE_DO_YOU_CLEAN)

		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.sourcePos = scrollSlotPos
		self.questionDialog.targetPos = targetSlotPos

	def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
		metinIndex = player.GetItemIndex(metinSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = player.CanAttachMetin(metinIndex, targetSlotPos)

		if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))

		if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))

		elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))

		elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.ATTACH_METIN_OK != result:
			return

		self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)



	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		overSlotPosGlobal = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		self.wndItem.SetUsableItem(False)

		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if player.SLOT_TYPE_INVENTORY == attachedItemType:

				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

				if attachedItemVNum==player.ITEM_MONEY: # @fixme005
					pass
				elif self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPosGlobal):
					self.wndItem.SetUsableItem(True)
					self.ShowToolTip(overSlotPosGlobal)
					return

		self.ShowToolTip(overSlotPosGlobal)


	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		if item.IsRefineScroll(srcItemVNum):
			return True
		elif item.IsMetin(srcItemVNum):
			return True
		elif item.IsDetachScroll(srcItemVNum):
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		elif constInfo.ENABLE_SELF_STACK_SCROLLS and srcItemVNum in (71052,71051,71084,71085):
			return True
		else:
			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True
			if app.ENABLE_GROWTH_PET_SYSTEM:
				if self.__IsUsablePetItem(srcItemVNum):
					return True

		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		if srcSlotPos == dstSlotPos:
			return False

		if item.IsRefineScroll(srcItemVNum):
			if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
				return True
			elif constInfo.ENABLE_SELF_STACK_SCROLLS and player.GetItemIndex(dstSlotPos) == srcItemVNum:
				return True
		elif item.IsMetin(srcItemVNum):
			if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
				return True
		elif item.IsDetachScroll(srcItemVNum):
			if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if player.CanUnlock(srcItemVNum, dstSlotPos):
				return True

		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True

		elif constInfo.ENABLE_SELF_STACK_SCROLLS and srcItemVNum in (71052,71051,71084,71085):
			return True

		else:
			if app.ENABLE_GROWTH_PET_SYSTEM:
				if self.__CanUseSrcPetItemToDstPetItem(srcItemVNum, srcSlotPos, dstSlotPos):
					return True

			useType=item.GetUseType(srcItemVNum)

			if "USE_CLEAN_SOCKET" == useType:
				if self.__CanCleanBrokenMetinStone(dstSlotPos):
					return True
			elif "USE_CHANGE_ATTRIBUTE" == useType:
				if self.__CanChangeItemAttrList(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ACCESSORY_SOCKET" == useType:
				if self.__CanAddAccessorySocket(dstSlotPos):
					return True
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:
				if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
					return True;
			elif "USE_PUT_INTO_BELT_SOCKET" == useType:
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				print "USE_PUT_INTO_BELT_SOCKET", srcItemVNum, dstItemVNum

				item.SelectItem(dstItemVNum)

				if item.ITEM_TYPE_BELT == item.GetItemType():
					return True
			elif app.ENABLE_USE_COSTUME_ATTR and "USE_CHANGE_COSTUME_ATTR" == useType:
				if self.__CanChangeCostumeAttrList(dstSlotPos):
					return True
			elif app.ENABLE_USE_COSTUME_ATTR and "USE_RESET_COSTUME_ATTR" == useType:
				if self.__CanResetCostumeAttr(dstSlotPos):
					return True

		return False

	def __CanCleanBrokenMetinStone(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.ITEM_TYPE_WEAPON != item.GetItemType():
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
				return True

		return False

	def __CanChangeItemAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
				return True

		return False

	if app.ENABLE_USE_COSTUME_ATTR:
		def __CanChangeCostumeAttrList(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if item.GetItemType() != item.ITEM_TYPE_COSTUME:
				return False

			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
					return True

			return False

		def __CanResetCostumeAttr(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if item.GetItemType() != item.ITEM_TYPE_COSTUME:
				return False

			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
					return True

			return False

	def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
			return False

		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False

		return True

	def __CanAddItemAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		attrCount = 0
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
				attrCount += 1

		if attrCount<4:
			return True

		return False

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def UseItemSlot(self, slotIndex):
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), 1)
				return
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if self.isShowAcceWindow():
				acce.Add(player.INVENTORY, slotIndex, 255)
				return

		self.__UseItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def __UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(slotIndex)
		item.SelectItem(ItemVNum)

		if app.WJ_ENABLE_TRADABLE_ICON:
			if self.interface.AttachInvenItemToOtherWindowSlot(slotIndex):
				return

		if app.ENABLE_GROWTH_PET_SYSTEM:
			itemType = item.GetItemType()

			if self.interface.wndPetInfoWindow.AttachItemToPetWindow(player.INVENTORY, slotIndex):
				return

			if self.PetSkillDelDlg and self.PetSkillDelDlg.IsShow():
				self.__PetSkillDeleteQuestionDialogCancel()

			if item.ITEM_TYPE_PET == itemType:
				self.__UseItemPet(slotIndex)
				return

		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		else:
			self.__SendUseItemPacket(slotIndex)
			#net.SendItemUsePacket(slotIndex)

	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		dstItemVNum = player.GetItemIndex(dstSlotPos)
		srcItemVNum = player.GetItemIndex(srcSlotPos)
		if constInfo.ENABLE_SELF_STACK_SCROLLS and dstItemVNum == srcItemVNum:
			self.__SendMoveItemPacket(srcSlotPos, dstSlotPos, 0)
		else:
			net.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)

	def __SendUseItemPacket(self, slotPos):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUsePacket(slotPos)

	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)

	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoulRefine = wndDragonSoulRefine

	def OnMoveWindow(self, x, y):
		# print "Inventory Global Pos : ", self.GetGlobalPosition()
		if self.wndBelt:
			# print "Belt Global Pos : ", self.wndBelt.GetGlobalPosition()
			self.wndBelt.AdjustPositionAndSize()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def SetAcceWindow(self, wndAcceCombine, wndAcceAbsorption):
			self.wndAcceCombine = wndAcceCombine
			self.wndAcceAbsorption = wndAcceAbsorption

		def isShowAcceWindow(self):
			if self.wndAcceCombine:
				if self.wndAcceCombine.IsShow():
					return 1
			if self.wndAcceAbsorption:
				if self.wndAcceAbsorption.IsShow():
					return 1
			return 0

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def __UseItemPet(self, slotIndex):
			itemSubType = item.GetItemSubType()
			if item.PET_EGG == itemSubType:
				self.petHatchingWindow.HatchingWindowOpen(player.INVENTORY, slotIndex)

			elif item.PET_UPBRINGING == itemSubType:
				if self.__CanUseGrowthPet(slotIndex):
					self.__SendUseItemPacket(slotIndex)

			elif item.PET_PAY == itemSubType:
				self.__SendUseItemPacket(slotIndex)

			elif item.PET_BAG == itemSubType:
				if self.__CanUsePetBagItem(slotIndex):
					if self.questionDialog:
						self.questionDialog.Close()

					self.questionDialog = uiCommon.QuestionDialog()
					self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_PET_BAG_TAKE_OUT)
					self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
					self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
					self.questionDialog.slotIndex = slotIndex
					self.questionDialog.Open()

			if item.PET_SKILL_ALL_DEL_BOOK == itemSubType:
				pet_id = player.GetActivePetItemId()
				if 0 == pet_id:
					return
				(skill_count, pet_skill1, pet_skill_level1, pet_skill_cool1, pet_skill2, pet_skill_level2, pet_skill_cool2, pet_skill3, pet_skill_level3, pet_skill_cool3) = player.GetPetSkill(pet_id)
				if 0 == pet_skill1 and 0 == pet_skill2 and 0 == pet_skill3:
					popup = uiCommon.PopupDialog()
					popup.SetText(localeInfo.PET_EMPTY_SKILL_SLOT_USE_ITEM)
					popup.SetAcceptEvent(self.__OnClosePopupDialog)
					popup.Open()
					self.pop = popup
					return

				self.PetSkillAllDelBookIndex = slotIndex
				self.SetCantMouseEventSlot( self.PetSkillAllDelBookIndex )

				self.PetSkillDelDlg.SetAcceptEvent(ui.__mem_func__(self.__PetSkillDeleteQuestionDialogAccept))
				self.PetSkillDelDlg.SetCancelEvent(ui.__mem_func__(self.__PetSkillDeleteQuestionDialogCancel))

				self.PetSkillDelDlg.SetText1( localeInfo.PET_SKILL_DELETE_QUESTION_DLG_MSG1 )
				self.PetSkillDelDlg.SetText2( localeInfo.PET_SKILL_DELETE_QUESTION_DLG_MSG2 )
				(w,h) = self.PetSkillDelDlg.GetTextSize1()
				self.PetSkillDelDlg.SetWidth(w+100)
				self.PetSkillDelDlg.Open()

		def __OnClosePopupDialog(self):
			self.pop = None

		def __ActivePetHighlightSlot(self, slotNumber):
			active_id = player.GetActivePetItemId()

			if active_id == player.GetItemMetinSocket(player.INVENTORY, slotNumber, 2):

				if slotNumber >= player.INVENTORY_PAGE_SIZE:
					slotNumber -= (self.inventoryPageIndex * player.INVENTORY_PAGE_SIZE)

				self.wndItem.ActivateSlot(slotNumber)
			else:
				if slotNumber >= player.INVENTORY_PAGE_SIZE:
					slotNumber -= (self.inventoryPageIndex * player.INVENTORY_PAGE_SIZE)

				self.wndItem.DeactivateSlot(slotNumber)

		def __SetCoolTimePetItemSlot(self, slotNumber, itemVnum):

			item.SelectItem(itemVnum)
			itemSubType = item.GetItemSubType()

			if itemSubType not in [item.PET_UPBRINGING, item.PET_BAG]:
				return

			if itemSubType == item.PET_BAG:
				id = player.GetItemMetinSocket(player.INVENTORY, slotNumber, 2)
				if id == 0:
					return

			(limitType, limitValue) = item.GetLimit(0)

			if itemSubType == item.PET_UPBRINGING:
				limitValue = player.GetItemMetinSocket(player.INVENTORY, slotNumber, 1)

			if limitType in [item.LIMIT_REAL_TIME, item.LIMIT_REAL_TIME_START_FIRST_USE]:

				sock_time   = player.GetItemMetinSocket(player.INVENTORY, slotNumber, 0)

				remain_time = max(0, sock_time - app.GetGlobalTimeStamp())

				if slotNumber >= player.INVENTORY_PAGE_SIZE:
					slotNumber -= (self.inventoryPageIndex * player.INVENTORY_PAGE_SIZE)

				self.wndItem.SetSlotCoolTimeInverse(slotNumber, limitValue, limitValue - remain_time)

		def __IsPetItem(self, srcItemVID):
			item.SelectItem(srcItemVID)

			if item.GetItemType() == item.ITEM_TYPE_PET:
				return True

			return False

		def __SendUsePetItemToItemPacket(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
			if self.__CanUseSrcPetItemToDstPetItem(srcItemVID, srcItemSlotPos, dstItemSlotPos):
				srcItemVnum		= player.GetItemIndex(srcItemSlotPos)
				item.SelectItem( srcItemVnum )
				srcItemType		= item.GetItemType()
				srcItemSubType	= item.GetItemSubType()

				if item.ITEM_TYPE_PET == srcItemType:					
					if srcItemSubType in [item.PET_FEEDSTUFF, item.PET_BAG]:
						self.__OpenPetItemQuestionDialog(srcItemSlotPos, dstItemSlotPos)
					elif item.PET_NAME_CHANGE == srcItemSubType:
						self.__UseItemPetNameChange(srcItemSlotPos, dstItemSlotPos)
				return True

			return False

		def __UseItemPetNameChange(self, srcSlotPos, dstSlotPos):
			if self.petNameChangeWindow:
				self.petNameChangeWindow.NameChangeWindowOpen(srcSlotPos, dstSlotPos)

		def __IsUsablePetItem(self, srcItemVNum):
			item.SelectItem(srcItemVNum)
			srcItemType		= item.GetItemType()
			srcItemSubType	= item.GetItemSubType()

			if srcItemType != item.ITEM_TYPE_PET:
				return False

			if srcItemSubType not in [item.PET_UPBRINGING, item.PET_FEEDSTUFF, item.PET_BAG, item.PET_NAME_CHANGE]:
				return False

			return True

		def __CanUseSrcPetItemToDstPetItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
			item.SelectItem(srcItemVNum)
			srcItemType		= item.GetItemType()
			srcItemSubType	= item.GetItemSubType()

			if srcItemType != item.ITEM_TYPE_PET:
				return False

			if srcItemSubType == item.PET_FEEDSTUFF:		
				detIndex = player.GetItemIndex(dstSlotPos)
				item.SelectItem(detIndex)

				dstItemType		= item.GetItemType()
				dstItemSubType	= item.GetItemSubType()

				if dstItemType != item.ITEM_TYPE_PET:
					return False

				if dstItemSubType not in [item.PET_UPBRINGING]:
					return False

				if dstItemSubType == item.PET_BAG:
					incaseTime = player.GetItemMetinSocket(dstSlotPos, 1)
					if incaseTime == 0:
						return False

			elif srcItemSubType == item.PET_BAG:
				detIndex = player.GetItemIndex(dstSlotPos)
				item.SelectItem(detIndex)

				dstItemType		= item.GetItemType()
				dstItemSubType	= item.GetItemSubType()

				if dstItemType != item.ITEM_TYPE_PET:
					return False

				if dstItemSubType not in [item.PET_UPBRINGING, item.PET_BAG]:
					return False

				lifeTime = player.GetItemMetinSocket(dstSlotPos, 0)

				if dstItemSubType == item.PET_UPBRINGING:
					if lifeTime < app.GetGlobalTimeStamp():
						return False

					srcIncase = player.GetItemMetinSocket(srcSlotPos, 1)
					if srcIncase != 0:
						return False

				elif dstItemSubType == item.PET_BAG:
					if lifeTime > app.GetGlobalTimeStamp():
						return False

					srcIncase = player.GetItemMetinSocket(srcSlotPos, 1)
					if srcIncase != 0:
						return False

					destIncase = player.GetItemMetinSocket(dstSlotPos, 1)
					if destIncase == 0:
						return False

			elif srcItemSubType == item.PET_NAME_CHANGE:
				detIndex = player.GetItemIndex(dstSlotPos)
				item.SelectItem(detIndex)

				dstItemType		= item.GetItemType()
				dstItemSubType	= item.GetItemSubType()

				if dstItemType != item.ITEM_TYPE_PET:
					return False

				if dstItemSubType not in [item.PET_UPBRINGING]:
					return False

			else:
				return False

			return True

		def __CanUseGrowthPet(self, slotIndex):
			if not player.GetItemMetinSocket(player.INVENTORY, slotIndex, 2):
				return False

			(limitType, limitValue) = item.GetLimit(0)
			remain_time = 999
			if item.LIMIT_REAL_TIME == limitType:
				sock_time   = player.GetItemMetinSocket(player.INVENTORY, slotIndex, 0)
				if app.GetGlobalTimeStamp() > sock_time:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_SUMMON_BECAUSE_LIFE_TIME_END)
					return False

			return True

		def __CanUsePetBagItem(self, slotIndex):
			if not player.GetItemMetinSocket(player.INVENTORY, slotIndex, 2):
				return False

			(limitType, limitValue) = item.GetLimit(0)
			remain_time = 999
			if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
				sock_time	= player.GetItemMetinSocket(player.INVENTORY, slotIndex, 0)
				use_cnt		= player.GetItemMetinSocket(player.INVENTORY, slotIndex, 1)

				if use_cnt:
					if app.GetGlobalTimeStamp() > sock_time:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_USE_BAG)
						return False;

			return True

		def __CanAttachGrowthPetItem(self, itemVNum, itemSlotIndex):
			activePetId = player.GetActivePetItemId()
			if activePetId == 0:
				return True

			item.SelectItem(itemVNum)
			itemType	= item.GetItemType()
			itemSubType = item.GetItemSubType()

			if item.ITEM_TYPE_PET == itemType and itemSubType == item.PET_UPBRINGING:
				petId = player.GetItemMetinSocket(itemSlotIndex, 2)
				if petId == activePetId:
					return False

			return True

		def SetPetHatchingWindow(self, window):
			self.petHatchingWindow = window

		def SetPetNameChangeWindow(self, window):
			self.petNameChangeWindow = window

		def SetPetFeedWindow(self, window):
			self.petFeedWindow = window

		def ItemMoveFeedWindow(self, slotWindow, slotIndex):
			if not self.petFeedWindow:
				return

			self.petFeedWindow.ItemMoveFeedWindow(slotWindow, slotIndex)

		def __OpenPetBagQuestionDialog(self, srcItemSlotPos, dstItemSlotPos):
			if self.interface.IsShowDlgQuestionWindow():
				self.interface.CloseDlgQuestionWindow()

		def __OpenPetItemQuestionDialog(self, srcItemPos, dstItemPos):
			if self.interface.IsShowDlgQuestionWindow():
				self.interface.CloseDlgQuestionWindow()

			getItemVNum=player.GetItemIndex
			self.srcItemPos = srcItemPos
			self.dstItemPos = dstItemPos

			srcItemVnum = getItemVNum(srcItemPos)
			dstItemVnum = getItemVNum(dstItemPos)

			item.SelectItem( srcItemVnum )
			src_item_name = item.GetItemName( srcItemVnum )
			srcItemType		= item.GetItemType()
			srcItemSubType	= item.GetItemSubType()

			item.SelectItem( dstItemVnum )
			dst_item_name = item.GetItemName( getItemVNum(dstItemPos) )

			self.PetItemQuestionDlg.SetAcceptEvent(ui.__mem_func__(self.__PetItemAccept))
			self.PetItemQuestionDlg.SetCancelEvent(ui.__mem_func__(self.__PetItemCancel))

			if item.ITEM_TYPE_PET == srcItemType:
				if item.PET_FEEDSTUFF == srcItemSubType:
					self.PetItemQuestionDlg.SetText( localeInfo.INVENTORY_REALLY_USE_PET_FEEDSTUFF_ITEM % ( src_item_name, dst_item_name ) )
					self.PetItemQuestionDlg.Open()

				elif item.PET_BAG == srcItemSubType:
					self.PetItemQuestionDlg.SetText( localeInfo.INVENTORY_REALLY_USE_PET_BAG_ITEM )
					self.PetItemQuestionDlg.Open()			

		def __PetItemAccept(self):
			self.PetItemQuestionDlg.Close()
			self.__SendUseItemToItemPacket(self.srcItemPos, self.dstItemPos)
			self.srcItemPos = (0, 0)
			self.dstItemPos = (0, 0)
			self.srcItemWindow = None
			self.dstItemWindow = None

		def __PetItemCancel(self):
			self.srcItemPos = (0, 0)
			self.dstItemPos = (0, 0)
			self.PetItemQuestionDlg.Close()

		def __PetSkillDeleteQuestionDialogAccept(self):
			net.SendPetDeleteAllSkill( self.PetSkillAllDelBookIndex )	
			self.__PetSkillDeleteQuestionDialogCancel()

		def __PetSkillDeleteQuestionDialogCancel(self):
			self.PetSkillDelDlg.Close()
			self.SetCanMouseEventSlot( self.PetSkillAllDelBookIndex )
			self.PetSkillAllDelBookIndex = -1

		def SetCanMouseEventSlot(self, inven_slot_index):
			if inven_slot_index >= player.INVENTORY_PAGE_SIZE:
				page = self.GetInventoryPageIndex() # range 0,1,2,3
				inven_slot_index -= (page * player.INVENTORY_PAGE_SIZE)
			self.wndItem.SetCanMouseEventSlot(inven_slot_index)

		def SetCantMouseEventSlot(self, inven_slot_index):
			if inven_slot_index >= player.INVENTORY_PAGE_SIZE:
				page = self.GetInventoryPageIndex() # range 0,1,2,3
				inven_slot_index -= (page * player.INVENTORY_PAGE_SIZE)
			self.wndItem.SetCantMouseEventSlot(inven_slot_index)

	def IsDlgQuestionShow(self):
		if self.dlgQuestion.IsShow():
			return True

		return False

	def CancelDlgQuestion(self):
		self.__Cancel()
