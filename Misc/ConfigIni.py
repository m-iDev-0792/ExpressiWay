import os

########################################################################
class ConfigItem:
    Line:str = ""
    Name:str = ""
    Value:str = ""
    Values = []

    def __init__(self):
        self.Line = ""
        self.Name = ""
        self.Value = ""
        self.Values = []
        pass

########################################################################
class ConfigSection:
    Name:str = ""
    Items = {}

    def __init__(self):
        self.Name = ""
        self.Items = {}
        pass

    def GetItemValue(self, key:str)->str:
        item = self.Items.get(key)
        if not item == None:
            return item.Value
        pass
        return ""

    
    def GetItemValues(self, key:str):
        item  = self.Items.get(key)
        if not item == None:
            return item.Values
        pass
        return []

    def GetItemLine(self, key:str)->str:
        item = self.Items.get(key)
        if not item == None:
            return item.Line
        pass
        return ""

    def AddItem(self, key:str, item:ConfigItem):
        if self.Items.get(key) == None:
            self.Items[key] = item
        else:
            self.Items[key] = item
        pass

    def AppendItem(self, key:str, value:str):
        item = self.Items.get(key)
        if item == None:
            item = ConfigItem()
            item.Name = key
            self.Items[key] = item
        pass
        item.Values.append(value)
        pass



########################################################################
class ConfigIni:
    Sections = {}

    def __init__(self):
        self.Sections = {}
        pass


    def TrimNotes(line:str)->str:
        pos = line.find(';')
        if pos < 0 : return line
        if pos == 0: return "" 
        return line[0:pos-1]

    def Load(self, path:str):
        if not os.path.exists(path):
            print("ConfigIni.Load() File Don't Exist:",path)
            return
        pass

        f_in = open(path,'r', encoding="utf-8-sig")
        lines = f_in.readlines()

        cursec = None
        for it in lines:
            line = ConfigIni.TrimNotes(it)
            line = line.strip()
            if line == "" or line == None:
                continue
            pass
            
            if line.startswith("["):
                secname = ""
                pos = line.find("]")
                if pos > 0:
                    secname = line[1:pos]
                pass

                if secname != "":
                    if self.Sections.get(secname) == None:
                        cursec = ConfigSection()
                        cursec.Name = secname
                        self.Sections[secname] = cursec
                    else:
                        cursec = self.Sections.get(secname)
                    pass
                pass
                
                continue
            pass

            if cursec != None:
                if line.startswith('+'):
                    pos = line.find('=')
                    name = line[1: pos]
                    value = line[pos+1:]
                    cursec.AppendItem(name, value)
                elif line.startswith('-'):
                    item = ConfigItem()
                    item.Line = line
                    cursec.AddItem(line, item)
                else:
                    pos = line.find('=')
                    if pos > 0:
                        name = line[0:pos]
                        value = line[pos+1:]
                        item = ConfigItem()
                        item.Line = line
                        item.Name = name
                        item.Value = value
                        cursec.AddItem(name,item)
                    else:
                        item = ConfigItem()
                        item.Line = line
                        cursec.AddItem(line, item)
                    pass
                pass
            pass

        pass


    def GetSection(self, name:str)->ConfigSection:
        return self.Sections.get(name)

    def GetItemValue(self, section:str, key:str)->str:
        secobj:ConfigSection = self.Sections.get(section)
        if secobj != None:
            return secobj.GetItemValue(key)
        pass
        return ""


########################################################################    
GConfig = ConfigIni()