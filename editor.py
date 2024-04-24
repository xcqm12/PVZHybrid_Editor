from pymem import Pymem
import win32gui
import win32process
import psutil
import re
import time
import os
import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.tooltip import ToolTip
import PVZ_data as data
import PVZ_Hybrid as pvz

data.update_PVZ_memory(1)
zombie_select=None

def resource_path(relative_path):
    """ 获取资源的绝对路径，适用于开发环境和PyInstaller环境 """
    try:
        # PyInstaller创建的临时文件夹的路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def chooseGame():
    def openPVZ_memory(process1):
        try:
            data.update_PVZ_memory(Pymem(int(re.search(r'(\d+)',process1).group(1))))
        except:
            Messagebox.show_error("没有足够的权限，请确保游戏未以管理员身份运行",title="注入进程失败",parent=choose_process_window)
            choose_process_window.quit()
            choose_process_window.destroy()
        else:   
            choose_process_window.quit()
            choose_process_window.destroy()   

    def tryFindGame():
        try:
            hwnd=win32gui.FindWindow("MainWindow",None)
            pid=win32process.GetWindowThreadProcessId(hwnd)
            data.update_PVZ_memory( Pymem(pid[1]))
            choose_process_window.quit()
            choose_process_window.destroy()
        except:
            Messagebox.show_error("请确保游戏已开启且未以管理员身份运行\n如果仍无法注入游戏可以尝试使用管理员身份开启本修改器",title="未找到游戏",parent=choose_process_window)
            return

    # def retry():
    #     global PVZ_memory
    #     choose_process_window.quit()
    #     choose_process_window.destroy()
    #     data.update_PVZ_memory(1
    #     # choosegame()
    #     return PVZ_memory

    def close():
        choose_process_window.quit()
        choose_process_window.destroy()
        data.update_PVZ_memory(0)
     
    def getSelecthwnd():
        hwnd_title = dict() 
        def get_all_hwnd(hwnd,mouse):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
        win32gui.EnumWindows(get_all_hwnd, 0)
        selecthwnd=list()
        for h,t in hwnd_title.items():
            if t != "":
                pid=win32process.GetWindowThreadProcessId((h))
                pn=psutil.Process(pid[1]).name()
                selecthwnd.append((pid[1],[t],[pn]))
        return selecthwnd
    
    choose_process_window = ttk.Toplevel(topmost=True)
    choose_process_window.title("选择进程")
    choose_process_window.geometry("500x500")
    choose_process_window.iconphoto(False,ttk.PhotoImage(file=resource_path(r"res\icon\choose.png")))
    label = ttk.Label(choose_process_window,text="如果未开启游戏请开启游戏后点击寻找游戏按钮",bootstyle=WARNING, font=("黑体", 16))
    label.pack(pady=20)
    frame1 = ttk.Frame(choose_process_window)
    frame1.pack()
    retry_button = ttk.Button(frame1, text='寻找游戏', command=lambda:tryFindGame())
    retry_button.pack(side=LEFT,padx=80)
    close_button = ttk.Button(frame1, text='关闭',bootstyle=DANGER, command=lambda:close())
    close_button.pack(side=RIGHT,padx=80)
    label = ttk.Label(choose_process_window,text="如有需要可在下方手动选择游戏窗口\n窗口名一般为植物大战僵尸杂交版\n进程名一般为PlantsVsZombies.exe\n显示格式为pid 窗口名 进程名",bootstyle=INFO, font=("黑体", 16))
    label.pack(pady=(50,10))
    frame2 = ttk.Frame(choose_process_window)
    frame2.pack()
    combobox = ttk.Combobox(frame2,bootstyle=PRIMARY,width=50)
    combobox.pack(side=LEFT)
    def refreshList():
        selecthwnd=getSelecthwnd()
        #设置下拉菜单中的值
        combobox['state'] = NORMAL
        combobox['value'] = (selecthwnd)
        combobox['state'] = READONLY
    #设置下拉菜单的默认值,默认值索引从0开始
        combobox.current(0)
    refreshList()
    refresh_button = ttk.Button(frame2, text='刷新列表',bootstyle=INFO, command=lambda:refreshList())
    refresh_button.pack(side=LEFT,padx=(10,0))
    comfrime_button = ttk.Button(choose_process_window, text='确定',bootstyle=SUCCESS, command=lambda:openPVZ_memory(combobox.get()))
    comfrime_button.pack(pady=(30,0))
    choose_process_window.protocol('WM_DELETE_WINDOW',lambda:close())
    choose_process_window.mainloop()

def mainWindow():
    main_window=ttk.Window()
    main_window.title("杂交版多功能修改器")
    main_window.geometry("500x500")
    main_window.iconphoto(False,ttk.PhotoImage(file=resource_path(r"res\icon\editor.png")))
    # style=ttk.Style()
    # style.configure('small.TButton',font=("黑体",8),padding=(0,0,0,0))
    process_frame=ttk.Frame(main_window)
    process_frame.place(x=0,y=0,relx=1,rely=1,anchor=SE)
    process_label=ttk.Label(process_frame,text="", font=("黑体", 8))
    process_label.pack(side=LEFT)
    def updateGame():
        chooseGame()
        if(type(data.PVZ_memory)!= Pymem):
            process_label["text"]="未找到游戏"
            process_label.config(bootstyle=DANGER)
        else:
            process_label["text"]="找到进程："+str(data.PVZ_memory.process_id)+str(psutil.Process(data.PVZ_memory.process_id).name())
            process_label.config(bootstyle=DANGER)
    def tryFindGame():
        try:
            hwnd=win32gui.FindWindow("MainWindow",None)
            pid=win32process.GetWindowThreadProcessId(hwnd)
            data.update_PVZ_memory( Pymem(pid[1]))
            process_label["text"]="找到进程："+str(data.PVZ_memory.process_id)+str(psutil.Process(data.PVZ_memory.process_id).name())
            process_label.config(bootstyle=DANGER)
        except:
            updateGame()
    tryFindGame()
    choose_process_button=ttk.Button(process_frame,text="选择游戏",padding=0,bootstyle=(PRIMARY,LINK),command=lambda:updateGame())
    choose_process_button.pack(side=LEFT)
    back_ground_status=ttk.IntVar(main_window)
    back_ground_check=ttk.Checkbutton(main_window,text="后台运行",variable=back_ground_status,bootstyle="round-toggle",command=lambda:pvz.backGround(back_ground_status.get()))
    back_ground_check.place(x=3,y=-3,relx=0,rely=1,anchor=SW)
    
    
    page_tab=ttk.Notebook(main_window)
    page_tab.pack(padx=10, pady=(5,30), fill=BOTH,expand=True)
    common_page=ttk.Frame(page_tab)
    common_page.pack()
    page_tab.add(common_page,text="常用功能")
    resource_modify_frame=ttk.Labelframe(common_page,text="资源修改",bootstyle=WARNING)
    resource_modify_frame.place(x=0,y=0,anchor=NW)
    ttk.Label(resource_modify_frame,text="阳光：",bootstyle=WARNING,font=("宋体",14)).grid(row=0,column=0,sticky=E)
    sun=ttk.IntVar(main_window)
    sun_value=ttk.Entry(resource_modify_frame,width=8,bootstyle=WARNING,textvariable=sun)
    sun_value.grid(row=0,column=1)
    ttk.Button(resource_modify_frame,text="修改",bootstyle=(WARNING,OUTLINE),command=lambda:pvz.setSun(sun.get())).grid(row=0,column=2,padx=(5,0))
    ttk.Label(resource_modify_frame,text="增加阳光：",bootstyle=WARNING,font=("宋体",14)).grid(row=1,column=0,sticky=E)
    add_sun_value=ttk.Entry(resource_modify_frame,width=8,bootstyle=WARNING)
    add_sun_value.grid(row=1,column=1)
    ttk.Button(resource_modify_frame,text="增加",bootstyle=(WARNING,OUTLINE),command=lambda:pvz.addSun(int(add_sun_value.get()))).grid(row=1,column=2,padx=(5,0))
    
    quick_start_frame=ttk.LabelFrame(common_page,text="快速使用",bootstyle=SUCCESS)
    quick_start_frame.place(x=0,y=0,relx=1,rely=0,anchor=NE)
    over_plant_status=ttk.IntVar(quick_start_frame)
    over_plant_check=ttk.Checkbutton(quick_start_frame,text="自由放置",variable=over_plant_status,bootstyle="success-round-toggle",command=lambda:pvz.overPlant(over_plant_status.get()))
    over_plant_check.grid(row=0,column=0,sticky=W)
    ToolTip(over_plant_check,text="植物可以重叠放置并无视地形",bootstyle=(INFO,INVERSE))
    free_plant_status=ttk.IntVar(quick_start_frame)
    free_plant_check=ttk.Checkbutton(quick_start_frame,text="免费种植",variable=free_plant_status,bootstyle="success-round-toggle",command=lambda:pvz.ignoreSun(free_plant_status.get()))
    free_plant_check.grid(row=1,column=0,sticky=W)
    ToolTip(free_plant_check,text="植物可以不消耗阳光种植",bootstyle=(INFO,INVERSE))
    cancel_cd_status=ttk.IntVar(quick_start_frame)
    cancel_cd_check=ttk.Checkbutton(quick_start_frame,text="取消冷却",variable=cancel_cd_status,bootstyle="success-round-toggle",command=lambda:pvz.cancelCd(cancel_cd_status.get()))
    cancel_cd_check.grid(row=2,column=0,sticky=W)
    ToolTip(cancel_cd_check,text="植物种植后不进入冷却时间",bootstyle=(INFO,INVERSE))
    auto_colect_status=ttk.IntVar(quick_start_frame)
    auto_colect_check=ttk.Checkbutton(quick_start_frame,text="自动收集",variable=auto_colect_status,bootstyle="success-round-toggle",command=lambda:pvz.autoCollect(auto_colect_status.get()))
    auto_colect_check.grid(row=3,column=0,sticky=W)
    ToolTip(auto_colect_check,text="自动收集自然掉落的阳光和僵尸掉落的金币",bootstyle=(INFO,INVERSE))
    column_like_status=ttk.IntVar(quick_start_frame)
    column_like_check=ttk.Checkbutton(quick_start_frame,text="柱子模式",variable=column_like_status,bootstyle="success-round-toggle",command=lambda:pvz.column(column_like_status.get()))
    column_like_check.grid(row=4,column=0,sticky=W)
    ToolTip(column_like_check,text="种植一个植物后在同一列的其他行种植相同的植物(可与自由放置配合使用)",bootstyle=(INFO,INVERSE))
    shovel_pro_status=ttk.IntVar(quick_start_frame)
    shovel_pro_check=ttk.Checkbutton(quick_start_frame,text="超级铲子",variable=shovel_pro_status,bootstyle="success-round-toggle",command=lambda:pvz.shovelpro(shovel_pro_status.get()))
    shovel_pro_check.grid(row=5,column=0,sticky=W)
    ToolTip(shovel_pro_check,text="铲掉植物返还其阳光消耗并触发亡语效果",bootstyle=(INFO,INVERSE))
    never_fail_status=ttk.IntVar(quick_start_frame)
    never_fail_check=ttk.Checkbutton(quick_start_frame,text="永不失败",variable=never_fail_status,bootstyle="success-round-toggle",command=lambda:pvz.ignoreZombies(never_fail_status.get()))
    never_fail_check.grid(row=6,column=0,sticky=W)
    ToolTip(never_fail_check,text="僵尸进家不判定游戏失败",bootstyle=(INFO,INVERSE))
    win_button=ttk.Button(quick_start_frame,text="当前关卡胜利",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.win())
    win_button.grid(row=7,column=0,sticky=W,pady=(2,2))
    ToolTip(win_button,text="当前的游戏关卡直接进行胜利结算",bootstyle=(INFO,INVERSE))
    kill_all_button=ttk.Button(quick_start_frame,text="秒杀所有僵尸",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.killAllZombies())
    kill_all_button.grid(row=8,column=0,sticky=W,pady=(2,2))
    ToolTip(kill_all_button,text="秒杀当前场上的所有僵尸",bootstyle=(INFO,INVERSE))
    unlock_button=ttk.Button(quick_start_frame,text="解锁全部植物",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.unlock())
    unlock_button.grid(row=9,column=0,sticky=W,pady=(2,2))
    ToolTip(unlock_button,text="在本次游戏中临时解锁图鉴中的所有植物(包括尚无法获得的隐藏植物)",bootstyle=(INFO,INVERSE))
    
    game_speed_frame=ttk.LabelFrame(common_page,text="游戏速度",bootstyle=PRIMARY)
    game_speed_frame.place(x=0,y=100,anchor=NW)
    game_speed_label=ttk.Label(game_speed_frame,text="1",bootstyle=PRIMARY)
    game_speed_label.grid(row=0,column=0)
    game_speed_frame.columnconfigure(0,minsize=30)
    game_speed_value=ttk.DoubleVar(game_speed_frame)
    game_speed_value.set(2)
    def changeSpeedValue(value):
        step=1
        adjusted_value = round(float(value) / step) * step
        game_speed_value.set(adjusted_value)
        if(game_speed_value.get()==0):
            game_speed_label.config(text="0.25")
        elif(game_speed_value.get()==1):
            game_speed_label.config(text="0.5")
        elif(game_speed_value.get()==2):
            game_speed_label.config(text="1")
        elif(game_speed_value.get()==3):
            game_speed_label.config(text="2")
        elif(game_speed_value.get()==4):
            game_speed_label.config(text="5")
        elif(game_speed_value.get()==5):
            game_speed_label.config(text="10")
        elif(game_speed_value.get()==6):
            game_speed_label.config(text="20")
        pvz.changeGameSpeed(game_speed_value.get())
    game_speed_scale=ttk.Scale(game_speed_frame,from_=0,to=6,orient=HORIZONTAL,variable=game_speed_value,command=changeSpeedValue)
    game_speed_scale.grid(row=0,column=1)
    
    global zombie_select
    zombie_page=ttk.Frame(page_tab)
    zombie_page.pack()
    page_tab.add(zombie_page,text="僵尸修改")    
    zombie_list_frame=ttk.LabelFrame(zombie_page,text="僵尸列表",bootstyle=DANGER)
    zombie_list_frame.place(x=0,y=0,anchor=NW,height=430,width=350)
    zombie_list_box_scrollbar=ttk.Scrollbar(zombie_list_frame,bootstyle=DANGER)
    zombie_list_box=ttk.Treeview(zombie_list_frame,show=TREE,selectmode=BROWSE,padding=0,columns=("zombie_list"),yscrollcommand=zombie_list_box_scrollbar.set,bootstyle=DANGER)
    zombie_list_box_scrollbar.configure(command=zombie_list_box.yview)
    zombie_list_box.place(x=0,y=0,anchor=NW,height=410,width=50)
    zombie_list_box_scrollbar.place(x=50,y=0,height=410,anchor=NW)
    zombie_list=list()
    def refresh_zombie_list():
        zombie_list.clear()
        zombie_list_box.delete(*zombie_list_box.get_children())
        try:
            zombie_num=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xa0)
        except:
            return
        i=0
        j=0
        while i<zombie_num:
            zombie_addresss=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x90)+0x15c*j
            zombie_exist=data.PVZ_memory.read_bytes(zombie_addresss+0xec,1)
            if(zombie_exist==b'\x00'):
                zombie_list.append(data.zombie(zombie_addresss))
                i=i+1
            j=j+1
        n=0
        for k in range(zombie_num):
            zombie_list_box.insert("",END,iid=n,text=str(zombie_list[k].no))
            if(zombie_select!=None):
                if(zombie_select.exist==b'\x00'):
                    if(zombie_select.no==zombie_list[k].no):
                        zombie_list_box.selection_set((str(n),))
            n=n+1

    refresh_zombie_list()
    zombie_attribute_frame=ttk.Frame(zombie_list_frame)
    zombie_attribute_frame.place(x=80,y=0,height=430,width=250)
    zombie_state_frame=ttk.Frame(zombie_attribute_frame)
    zombie_state_frame.grid(row=0,column=0,sticky=W)
    ttk.Label(zombie_state_frame,text="僵尸类型:").grid(row=0,column=0,sticky=W)
    zombie_type_value=ttk.IntVar(zombie_state_frame)
    zombie_type_entry=ttk.Entry(zombie_state_frame,textvariable=zombie_type_value,width=15,state=READONLY,bootstyle=SECONDARY)
    zombie_type_entry.grid(row=0,column=1,sticky=W)
    ttk.Label(zombie_state_frame,text="状态:").grid(row=0,column=2,sticky=W)
    zombie_state_value=ttk.IntVar(zombie_state_frame)
    zombie_state_entry=ttk.Entry(zombie_state_frame,textvariable=zombie_state_value,width=3,bootstyle=SECONDARY)
    zombie_state_entry.grid(row=0,column=3,sticky=W)
    def setState(event):
        zombie_select.setState(zombie_state_value.get())
        zombie_state_frame.focus_set()
    zombie_position_frame=ttk.LabelFrame(zombie_attribute_frame,text="位置",bootstyle=DANGER)
    zombie_position_frame.grid(row=1,column=0,columnspan=4)
    ttk.Label(zombie_position_frame,text="x坐标:").grid(row=0,column=0,sticky=W)
    zombie_x_value=ttk.IntVar(zombie_position_frame)
    zombie_x_entry=ttk.Entry(zombie_position_frame,textvariable=zombie_x_value,width=3,bootstyle=SECONDARY)
    zombie_x_entry.grid(row=0,column=1,sticky=W)
    def setX(event):
        zombie_select.setState(zombie_state_value.get())
        zombie_position_frame.focus_set()
    ttk.Label(zombie_position_frame,text="y坐标:").grid(row=0,column=2,sticky=W)
    zombie_y_value=ttk.IntVar(zombie_position_frame)
    zombie_y_entry=ttk.Entry(zombie_position_frame,textvariable=zombie_y_value,width=3,bootstyle=SECONDARY)
    zombie_y_entry.grid(row=0,column=3,sticky=W)
    def setY(event):
        zombie_select.setState(zombie_y_value.get())
        zombie_position_frame.focus_set()
    ttk.Label(zombie_position_frame,text="第").grid(row=0,column=4,sticky=W)
    zombie_state_value=ttk.IntVar(zombie_position_frame)
    zombie_state_entry=ttk.Entry(zombie_position_frame,textvariable=zombie_state_value,width=3,bootstyle=SECONDARY)
    zombie_state_entry.grid(row=0,column=5,sticky=W)
    ttk.Label(zombie_position_frame,text="行").grid(row=0,column=6,sticky=W)
    def setState(event):
        zombie_select.setState(zombie_state_value.get())
        zombie_position_frame.focus_set()
    
    zombie_hp_frame=ttk.LabelFrame(zombie_attribute_frame,text="血量",bootstyle=DANGER)
    zombie_hp_frame.grid(row=2,column=0,columnspan=4)
    ttk.Label(zombie_hp_frame,text="本体:").grid(row=0,column=0)
    zombie_hp_value=ttk.IntVar(zombie_hp_frame)
    zombie_hp_entry=ttk.Entry(zombie_hp_frame,textvariable=zombie_hp_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    zombie_hp_entry.grid(row=0,column=1,ipady=0)
    def setHP(event):
        zombie_select.setHP(zombie_hp_value.get())
        zombie_hp_frame.focus_set()
    zombie_hp_entry.bind("<Return>",setHP)
    zombie_hp_frame.grid_columnconfigure(2,minsize=50)
    zombie_hatHP_label=ttk.Label(zombie_hp_frame,text="帽子:")
    zombie_hatHP_label.grid(row=0,column=2)
    zombie_hatHP_value=ttk.IntVar(zombie_hp_frame)
    zombie_hatHP_entry=ttk.Entry(zombie_hp_frame,textvariable=zombie_hatHP_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    zombie_hatHP_entry.grid(row=0,column=3,ipady=0)
    def setHatHP(event):
        zombie_select.setHatHP(zombie_hatHP_value.get())
        zombie_hp_frame.focus_set()
    zombie_hatHP_entry.bind("<Return>",setHatHP)
    ttk.Label(zombie_hp_frame,text="铁门:").grid(row=0,column=4)
    zombie_doorHP_value=ttk.IntVar(zombie_hp_frame)
    zombie_doorHP_entry=ttk.Entry(zombie_hp_frame,textvariable=zombie_doorHP_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    zombie_doorHP_entry.grid(row=0,column=5,ipady=0)
    def setDoorHP(event):
        zombie_select.setDoorHP(zombie_doorHP_value.get())
        zombie_hp_frame.focus_set()
    zombie_doorHP_entry.bind("<Return>",setDoorHP)


    def get_zombie_select(event):
        global zombie_select
        try:
            index=int(zombie_list_box.selection()[0])
            zombie_select=zombie_list[index]
        except:
            return

    def get_zombie_attribute():
        global zombie_select
        if zombie_select!=None:
            zombie_type_value.set(str(zombie_select.type)+":"+data.zombiesType[zombie_select.type])
            if(zombie_attribute_frame.focus_get()!=zombie_state_entry):
                zombie_state_value.set(zombie_select.state)
            if(zombie_attribute_frame.focus_get()!=zombie_hp_entry):
                zombie_hp_value.set(zombie_select.hp)
            if(zombie_select.hatType==0):
                zombie_hatHP_label["text"]="无:"
            elif(zombie_select.hatType==1):
                zombie_hatHP_label["text"]="路障:"
            elif(zombie_select.hatType==2):
                zombie_hatHP_label["text"]="铁桶:"
            elif(zombie_select.hatType==3):
                zombie_hatHP_label["text"]="橄榄帽:"
            elif(zombie_select.hatType==4):
                zombie_hatHP_label["text"]="矿工帽:"
            elif(zombie_select.hatType==7):
                zombie_hatHP_label["text"]="雪橇车:"
            elif(zombie_select.hatType==8):
                zombie_hatHP_label["text"]="坚果:"
            elif(zombie_select.hatType==9):
                zombie_hatHP_label["text"]="高冰果:"
            elif(zombie_select.hatType==10):
                zombie_hatHP_label["text"]="钢盔:"
            elif(zombie_select.hatType==11):
                zombie_hatHP_label["text"]="绿帽:"
            else:
                zombie_hatHP_label["text"]=str(zombie_select.hatType)+"未知:"
            if(zombie_attribute_frame.focus_get()!=zombie_hatHP_entry):
                zombie_hatHP_value.set(zombie_select.hatHP)
            if(zombie_attribute_frame.focus_get()!=zombie_doorHP_entry):
                zombie_doorHP_value.set(zombie_select.doorHP)

    zombie_list_box.bind("<<TreeviewSelect>>",get_zombie_select)


    plant_page=ttk.Frame(page_tab)
    plant_page.pack()
    page_tab.add(plant_page,text="植物修改")    
    
    grid_page=ttk.Frame(page_tab)
    grid_page.pack()
    page_tab.add(grid_page,text="场地修改")


    def refreshData():
        if(page_tab.index('current')==0):
            if(pvz.getMap()!=False):        
                if(main_window.focus_get()!=sun_value):
                    sun.set(pvz.getSun())
        if(page_tab.index('current')==1):
            if(pvz.getMap()!=False):       
                refresh_zombie_list()
                get_zombie_attribute()
        main_window.after(100,refreshData)
        
    main_window.after(100,refreshData)
    main_window.mainloop()

if __name__ == '__main__':
    mainWindow()