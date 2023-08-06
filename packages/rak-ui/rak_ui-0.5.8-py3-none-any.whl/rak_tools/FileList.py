import wx
import string
import os

import shutil

try:
    from agw import customtreectrl as CT
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.customtreectrl as CT

ArtIDs = ["ADD_BOOKMARK",
          "DEL_BOOKMARK",
          "HELP_SIDE_PANEL",
          "HELP_SETTINGS",
          "HELP_BOOK",
          "HELP_FOLDER",
          "HELP_PAGE",
          "GO_BACK",
          "GO_FORWARD",
          "GO_UP",
          "GO_DOWN",
          "GO_TO_PARENT",
          "GO_HOME",
          "FILE_OPEN",
          "PRINT",
          "HELP",
          "TIP",
          "REPORT_VIEW",
          "LIST_VIEW",
          "NEW_DIR",
          "HARDDISK",
          "FLOPPY",
          "CDROM",
          "REMOVABLE",
          "FOLDER",
          "FOLDER_OPEN",
          "GO_DIR_UP",
          "EXECUTABLE_FILE",
          "NORMAL_FILE",
          "TICK_MARK",
          "CROSS_MARK",
          "ERROR",
          "QUESTION",
          "WARNING",
          "INFORMATION",
          "MISSING_IMAGE",
          ]

Event = None


class FileList(CT.CustomTreeCtrl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.SUNKEN_BORDER | wx.WANTS_CHARS,
                 agwStyle=CT.TR_HAS_BUTTONS | CT.TR_HAS_VARIABLE_ROW_HEIGHT,
                 log=None, rootPath=r"..\testscripts", eventBus=None, EVENT=None):
        CT.CustomTreeCtrl.__init__(self, parent, id, pos, size, style, agwStyle)

        self.SetBackgroundColour(wx.WHITE)
        self.eventBus = eventBus
        global Event
        Event = EVENT
        self.checkedItemPath = {}

        alldata = dir(CT)
        treestyles = []
        events = []
        for data in alldata:
            if data.startswith("TR_"):
                treestyles.append(data)
            elif data.startswith("EVT_"):
                events.append(data)
        self.events = events
        self.styles = treestyles
        self.item = None
        self.windowed_item = None

        il = wx.ImageList(16, 16)

        for items in ArtIDs:
            il.Add(wx.ArtProvider.GetBitmap(eval("wx.ART_{}".format(items)), wx.ART_TOOLBAR,
                                            (16, 16)))

        self.AssignImageList(il)
        self.count = 0
        self.log = log

        self.rootPath = os.path.abspath(rootPath)
        self.root = self.AddRoot(self.rootPath)

        self.SetPyData(self.root, None)
        self.SetItemImage(self.root, 24, CT.TreeItemIcon_Normal)
        self.SetItemImage(self.root, 13, CT.TreeItemIcon_Expanded)

        self.updateChild(self.root, self.rootPath)

        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.eventdict = {'BEGIN_DRAG': self.OnBeginDrag,
                          'BEGIN_LABEL_EDIT': self.OnBeginEdit,
                          'BEGIN_RDRAG': self.OnBeginRDrag,
                          'DELETE_ITEM': self.OnDeleteItem,
                          'END_DRAG': self.OnEndDrag,
                          'END_LABEL_EDIT': self.OnEndEdit,
                          'ITEM_ACTIVATED': self.OnActivate,
                          'ITEM_CHECKED': self.OnItemCheck,
                          'ITEM_CHECKING': self.OnItemChecking,
                          'ITEM_COLLAPSED': self.OnItemCollapsed,
                          'ITEM_COLLAPSING': self.OnItemCollapsing,
                          'ITEM_EXPANDED': self.OnItemExpanded,
                          'ITEM_EXPANDING': self.OnItemExpanding,
                          'ITEM_GETTOOLTIP': self.OnToolTip,
                          'ITEM_MENU': self.OnItemMenu,
                          'ITEM_RIGHT_CLICK': self.OnRightDown,
                          'KEY_DOWN': self.OnKey,
                          'SEL_CHANGED': self.OnSelChanged,
                          'SEL_CHANGING': self.OnSelChanging,
                          "ITEM_HYPERLINK": self.OnHyperLink}

        mainframe = wx.GetTopLevelParent(self)

        evt_2_func = {CT.EVT_TREE_ITEM_EXPANDED: self.OnItemExpanded,
                      CT.EVT_TREE_ITEM_EXPANDING: self.OnItemExpanding,
                      CT.EVT_TREE_ITEM_COLLAPSED: self.OnItemCollapsed,
                      CT.EVT_TREE_ITEM_COLLAPSING: self.OnItemCollapsing,
                      CT.EVT_TREE_SEL_CHANGED: self.OnSelChanged,
                      CT.EVT_TREE_SEL_CHANGING: self.OnSelChanging,
                      wx.EVT_RIGHT_DOWN: self.OnRightDown,
                      wx.EVT_RIGHT_UP: self.OnRightUp}

        if not hasattr(mainframe, "leftpanel"):
            for _evt, _func in evt_2_func.items():
                self.Bind(_evt, _func)

        else:
            for combos in mainframe.treeevents:
                self.binding_events(combos)

        if hasattr(mainframe, "leftpanel"):
            self.ChangeStyle(mainframe.treestyles)

        self.SelectItem(self.root)
        self.ExpandAll()

    def refreshTree(self, rootPath: str = None, filterValue: str = None):
        self.Freeze()
        self.DeleteAllItems()

        if rootPath and len(rootPath) > 0:
            self.rootPath = os.path.abspath(rootPath)
        self.root = self.AddRoot(self.rootPath)
        self.SetPyData(self.root, None)
        self.SetItemImage(self.root, 24, CT.TreeItemIcon_Normal)
        self.SetItemImage(self.root, 13, CT.TreeItemIcon_Expanded)

        self.updateChild(self.root, self.rootPath, filterValue)
        self.Thaw()
        self.ExpandAll()
        pass

    def ChangeStyle(self, combos):

        style = 0
        for combo in combos:
            if combo.GetValue() == 1:
                style = style | eval("CT." + combo.GetLabel())

        if self.GetAGWWindowStyleFlag() != style:
            self.SetAGWWindowStyleFlag(style)

    def updateChild(self, parent, parentPath, filterValue: str = None):
        for fileName in os.listdir(parentPath):
            abspath = os.path.join(parentPath, fileName)
            isdir = os.path.isdir(abspath)

            if isdir:
                if not fileName.startswith("."):
                    dirItem = self.AppendItem(parent, fileName, ct_type=1)
                    self.SetPyData(dirItem, None)
                    self.SetItemImage(dirItem, 24, CT.TreeItemIcon_Normal)
                    self.SetItemImage(dirItem, 13, CT.TreeItemIcon_Expanded)
                    self.updateChild(dirItem, abspath, filterValue)
                    if filterValue and len(filterValue) > 0:
                        if not self.ItemHasChildren(dirItem):
                            self.Delete(dirItem)
            else:
                if filterValue and len(filterValue) > 0:
                    if fileName.lower().find(filterValue.lower()) == -1:
                        continue
                if fileName.endswith(".py") or fileName.endswith(".ini") or fileName.endswith(".txt"):
                    fileItem = self.AppendItem(parent, fileName, ct_type=1)
                    self.SetPyData(fileItem, None)
                    self.SetItemImage(fileItem, 28, CT.TreeItemIcon_Normal)
        pass

    def getFullPath(self, item):
        fullPath = []
        while item:
            fullPath.append(self.GetItemText(item))
            item = item.GetParent()
        fullPath.reverse()
        return "\\".join(fullPath)

    def OnCompareItems(self, item1, item2):
        if self.GetItemText(item1) < self.GetItemText(item2):
            return -1
        elif self.GetItemText(item1) > self.GetItemText(item2):
            return 1
        else:
            return 0

    def binding_events(self, choice, recreate=False):

        value = choice.GetValue()
        text = choice.GetLabel()
        evt = "CT." + text
        binder = self.eventdict[text[9:]]
        if value != 1:
            self.Bind(eval(evt), None)
            if evt == "CT.EVT_TREE_BEGIN_RDRAG":
                self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
                self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        else:
            if evt == "CT.EVT_TREE_BEGIN_RDRAG":
                self.Bind(wx.EVT_RIGHT_DOWN, None)
                self.Bind(wx.EVT_RIGHT_UP, None)
            self.Bind(eval(evt), binder)

    def OnIdle(self, event):
        event.Skip()

    def OnRightDown(self, event):

        pt = event.GetPosition()
        item, flags = self.HitTest(pt)

        self.UpdateAllItemChecked()

        # for _path in self.checkedItemPath:
        # logger.debug("checkedItemPath= {}".format(_path))

        if item:
            self.item = item
            self.SelectItem(item)

    def OnRightUp(self, event):

        item = self.item

        if not item:
            event.Skip()
            return

        self.current = item
        _itemText = self.GetItemText(item)

        if _itemText.endswith(".py"):
            menu = wx.Menu()
            # menu.AppendSeparator()

            # tests script run/stop/pause
            item_run = menu.Append(wx.ID_ANY, 'Run "{}"'.format(self.GetItemText(self.current)))

            item_stop = menu.Append(wx.ID_ANY, "Stop")
            menu.AppendSeparator()

            if len(self.checkedItemPath) > 0:
                item_run_select = menu.Append(wx.ID_ANY,
                                              'Run selected files')
                item_save_select = menu.Append(wx.ID_ANY,
                                               'Save selected files')

                self.Bind(wx.EVT_MENU, self.OnItemRunSelect, item_run_select)
                self.Bind(wx.EVT_MENU, self.OnItemSaveSelect, item_save_select)
            menu.AppendSeparator()

            item_rename = menu.Append(wx.ID_ANY, "Rename...")
            item_delete = menu.Append(wx.ID_ANY, "Delete...")

            if item == self.GetRootItem():
                item_delete.Enable(False)

            self.Bind(wx.EVT_MENU, self.OnItemRun, item_run)
            self.Bind(wx.EVT_MENU, self.OnItemStop, item_stop)
            self.Bind(wx.EVT_MENU, self.OnItemRename, item_rename)
            self.Bind(wx.EVT_MENU, self.OnItemDelete, item_delete)

            self.PopupMenu(menu)
            menu.Destroy()
            return

        elif _itemText.endswith(".txt"):
            menu = wx.Menu()
            # menu.AppendSeparator()

            if len(self.checkedItemPath) > 0:
                item_run_select = menu.Append(wx.ID_ANY,
                                              'Run selected files')
                item_save_select = menu.Append(wx.ID_ANY,
                                               'Save selected files')

                self.Bind(wx.EVT_MENU, self.OnItemRunSelect, item_run_select)
                self.Bind(wx.EVT_MENU, self.OnItemSaveSelect, item_save_select)
            menu.AppendSeparator()

            item_rename = menu.Append(wx.ID_ANY, "Rename...")
            item_delete = menu.Append(wx.ID_ANY, "Delete...")

            if item == self.GetRootItem():
                item_delete.Enable(False)

            self.Bind(wx.EVT_MENU, self.OnItemRename, item_rename)
            self.Bind(wx.EVT_MENU, self.OnItemDelete, item_delete)

            self.PopupMenu(menu)
            menu.Destroy()
            return

        elif _itemText.endswith(".ini"):
            menu = wx.Menu()
            # menu.AppendSeparator()

            # tests script run/stop/pause
            item_run = menu.Append(wx.ID_ANY, 'Run "{}"'.format(self.GetItemText(self.current)))

            item_stop = menu.Append(wx.ID_ANY, "Stop")
            menu.AppendSeparator()

            if len(self.checkedItemPath) > 0:
                item_run_select = menu.Append(wx.ID_ANY,
                                              'Run selected files')
                item_save_select = menu.Append(wx.ID_ANY,
                                               'Save selected files')

                self.Bind(wx.EVT_MENU, self.OnItemRunSelect, item_run_select)
                self.Bind(wx.EVT_MENU, self.OnItemSaveSelect, item_save_select)
            menu.AppendSeparator()

            item_rename = menu.Append(wx.ID_ANY, "Rename...")
            item_delete = menu.Append(wx.ID_ANY, "Delete...")

            if item == self.GetRootItem():
                item_delete.Enable(False)

            self.Bind(wx.EVT_MENU, self.OnItemRun, item_run)
            self.Bind(wx.EVT_MENU, self.OnItemStop, item_stop)
            self.Bind(wx.EVT_MENU, self.OnItemRename, item_rename)
            self.Bind(wx.EVT_MENU, self.OnItemDelete, item_delete)

            self.PopupMenu(menu)
            menu.Destroy()
            return

        else:
            menu = wx.Menu()
            item_create_folder = menu.Append(wx.ID_ANY, "new folder")
            item_create = menu.Append(wx.ID_ANY, "new file (Empty)")
            item_create_with_temp = menu.Append(wx.ID_ANY, "new file (With template)")

            menu.AppendSeparator()

            if len(self.checkedItemPath) > 0:
                item_run_select = menu.Append(wx.ID_ANY,
                                              'Run selected files')
                item_save_select = menu.Append(wx.ID_ANY,
                                               'Save selected files')

                self.Bind(wx.EVT_MENU, self.OnItemRunSelect, item_run_select)
                self.Bind(wx.EVT_MENU, self.OnItemSaveSelect, item_save_select)
            menu.AppendSeparator()

            item_rename = menu.Append(wx.ID_ANY, "Rename...")
            item_delete = menu.Append(wx.ID_ANY, "Delete...")

            if item == self.GetRootItem():
                item_delete.Enable(False)

            self.Bind(wx.EVT_MENU, self.OnItemRename, item_rename)
            self.Bind(wx.EVT_MENU, self.OnItemDelete, item_delete)
            self.Bind(wx.EVT_MENU, self.OnItemCreateFile, item_create)
            self.Bind(wx.EVT_MENU, self.OnItemCreateFolder, item_create_folder)
            self.Bind(wx.EVT_MENU, self.OnItemCreateFileWithTemp, item_create_with_temp)

            self.PopupMenu(menu)
            menu.Destroy()
            return

    def OnItemDelete(self, event):

        strs = "Are You Sure You Want To Delete Item " + self.GetItemText(self.current) + "?"
        dlg = wx.MessageDialog(None, strs, 'Deleting Item',
                               wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_NO:
            dlg.Destroy()
            return

        dlg.Destroy()
        self.DeleteChildren(self.current)
        self.Delete(self.current)
        self.DeleteFile(self.getFullPath(self.current))
        self.current = None

    def OnItemCreateFile(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'newScript')
        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newFilePath = self.getFullPath(self.current) + "\\{}".format(newname)
            if not os.path.exists(newFilePath):
                with open(newFilePath, "w") as newFile:
                    pass
            newitem = self.AppendItem(self.current, newname, ct_type=1)
            self.SetPyData(newitem, None)
            self.SetItemImage(newitem, 28, CT.TreeItemIcon_Normal)
            self.EnsureVisible(newitem)

        dlg.Destroy()

    def OnItemCreateFileWithTemp(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming',
                                 'newScript')

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newFilePath = self.getFullPath(self.current) + "\\{}".format(newname)
            # TODO should we need to set temp file path in the config panel?
            tempFilePath = self.rootPath + "\\TEMPLATES\\template.py"
            if os.path.exists(newFilePath):
                self.eventBus.post(Event.ShowMessageDlg(msg="This file already exists."))
            elif not os.path.exists(tempFilePath):
                self.eventBus.post(Event.ShowMessageDlg(msg="The temp file does not exist in {}.".
                                                        format(tempFilePath)))
            else:
                shutil.copy(tempFilePath, newFilePath)
                newItem = self.AppendItem(self.current, newname, ct_type=1)
                self.SetPyData(newItem, None)
                self.SetItemImage(newItem, 28, CT.TreeItemIcon_Normal)
                self.EnsureVisible(newItem)

        dlg.Destroy()

    def OnSeparatorInsert(self, event):

        newitem = self.InsertSeparator(self.GetItemParent(self.current), self.current)
        self.EnsureVisible(newitem)

    def OnBeginEdit(self, event):

        # show how to prevent edit...
        item = event.GetItem()
        if item and self.GetItemText(item) == "The Root Item":
            wx.Bell()

            # Lets just see what's visible of its children
            cookie = 0
            root = event.GetItem()
            (child, cookie) = self.GetFirstChild(root)

            while child:
                (child, cookie) = self.GetNextChild(root, cookie)

            event.Veto()

    def OnEndEdit(self, event):

        # show how to reject edit, we'll not allow any digits
        for x in event.GetLabel():
            if x in string.digits:
                event.Veto()
                return

    def OnLeftDClick(self, event):
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        if os.path.isfile(self.getFullPath(item)):
            self.eventBus.post(Event.OpenScriptFile(self.GetItemText(item), self.getFullPath(item)))
        if item and (flags & CT.TREE_HITTEST_ONITEMLABEL):
            if self.GetAGWWindowStyleFlag() & CT.TR_EDIT_LABELS:
                self.EditLabel(item)
        event.Skip()

    def OnItemExpanded(self, event):

        item = event.GetItem()
        if item:
            pass

    def OnItemExpanding(self, event):

        item = event.GetItem()
        if item:
            if item == self.windowed_item:
                item.DeleteWindow()
            child = self.GetLastChild(item)
        event.Skip()

    def OnItemCollapsed(self, event):

        item = event.GetItem()
        if item:
            pass

    def OnItemCollapsing(self, event):

        item = event.GetItem()
        if item:
            if item == self.windowed_item:
                item.DeleteWindow()
                pass
        event.Skip()

    def OnSelChanged(self, event):

        self.item = event.GetItem()
        event.Skip()

    def OnSelChanging(self, event):

        item = event.GetItem()
        olditem = event.GetOldItem()

        if item:
            if not olditem:
                olditemtext = "None"
            else:
                olditemtext = self.GetItemText(olditem)

        event.Skip()

    def OnBeginDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            event.Allow()

    def OnBeginRDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            event.Allow()

    def OnEndDrag(self, event):

        self.item = event.GetItem()
        event.Skip()

    def OnDeleteItem(self, event):

        item = event.GetItem()

        if not item:
            return
        event.Skip()

    def OnItemCheck(self, event):
        item = event.GetItem()
        children = item.GetChildren()
        event.Skip()

    def UpdateAllItemChecked(self, parent: CT.GenericTreeItem = None):
        if not parent:
            self.checkedItemPath.clear()
            parent = self.root

        parent.IsChecked()
        for _child in parent.GetChildren():
            if not _child.HasChildren():
                full_path = self.getFullPath(_child)
                if os.path.isfile(full_path) and \
                        _child.IsChecked() and full_path not in self.checkedItemPath:
                    self.checkedItemPath[full_path] = self.GetItemText(_child)
            else:
                self.UpdateAllItemChecked(_child)

    def OnItemChecking(self, event):

        item = event.GetItem()
        event.Skip()

    def OnToolTip(self, event):

        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))

    def OnItemMenu(self, event):

        item = event.GetItem()

        event.Skip()

    def OnKey(self, event):

        keycode = event.GetKeyCode()
        keyname = eval("wx.{}".format(keycode))

        if keycode == wx.WXK_BACK:
            # self.log.write("OnKeyDown: HAHAHAHA! I Vetoed Your Backspace! HAHAHAHA\n")
            return

        if keyname is None:
            if "unicode" in wx.PlatformInfo:
                keycode = event.GetUnicodeKey()
                if keycode <= 127:
                    keycode = event.GetKeyCode()
                keyname = "\"" + chr(event.GetUnicodeKey()) + "\""
                if keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode - 1)

            elif keycode < 256:
                if keycode == 0:
                    keyname = "NUL"
                elif keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode - 1)
                else:
                    keyname = "\"%s\"" % chr(keycode)
            else:
                keyname = "unknown (%s)" % keycode

        event.Skip()

    def OnActivate(self, event):

        event.Skip()

    def OnHyperLink(self, event):
        item = event.GetItem()

    def OnTextCtrl(self, event):

        keycode = event.GetKeyCode()
        char = chr(keycode) if keycode < 256 else ''
        event.Skip()

    def OnComboBox(self, event):
        selection = event.GetEventObject().GetValue()
        event.Skip()

    def OnItemRun(self, event):
        if self.current is not None and not self.current.GetChildren():
            self.eventBus.post(Event.RunSingleScript(self.GetItemText(self.current),
                                                     self.getFullPath(self.current)))
        pass

    def OnItemRunSelect(self, event):
        self.eventBus.post(Event.RunMultipleScript(self.checkedItemPath))
        pass

    def OnItemSaveSelect(self, event):
        self.eventBus.post(Event.SaveMultipleScript(self.checkedItemPath))
        pass

    def OnItemStop(self, event):
        self.eventBus.post("", tag=Event.System.STOP.TAG)
        pass

    def OnItemPause(self, event):
        pass

    def DeleteFile(self, filePath: str = None):
        if os.path.isfile(filePath):
            os.remove(filePath)
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath)
        pass

    def OnItemRename(self, event):
        dlg = wx.TextEntryDialog(self, "Please Enter The New Name", 'Renaming',
                                 self.GetItemText(self.current))

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            shutil.move(self.getFullPath(self.current),
                        self.getFullPath(self.current.GetParent()) + "\\{}".format(newname))
            self.current.SetText(newname)

        dlg.Destroy()
        pass

    def OnItemCreateFolder(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The folder Name", 'Item Naming', 'newFolder')
        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newFilePath = self.getFullPath(self.current) + "\\{}".format(newname)
            if not os.path.exists(newFilePath):
                os.mkdir(newFilePath)
            dirItem = self.AppendItem(self.current, newname, ct_type=1)
            self.SetPyData(dirItem, None)
            self.SetItemImage(dirItem, 24, CT.TreeItemIcon_Normal)
            self.SetItemImage(dirItem, 13, CT.TreeItemIcon_Expanded)
        dlg.Destroy()
