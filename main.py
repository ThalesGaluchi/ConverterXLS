import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import os
from convert import convert_columns

 
class SimpleFrame(ttk.Frame):
    ''' Basic Frame used in the Window'''
    def __init__(self, container):
        super().__init__(container)
        self['borderwidth'] = 5
        self['relief'] = 'groove'
        self['padding'] = 10        
        
        
              
class SelectFrame(SimpleFrame):
    ''' Frame for the Selection of the Input file'''
    
    def __init__(self, container):
        super().__init__(container)        
        self.info_select = '1. Select an Excel file to convert.' 
        self.info_select_output = '2. Select the outpt folder and output filename.' 
        
        # Split Frame in 3 columns (1,3,1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=7)
        self.columnconfigure(3, weight=1)        
        
        self.input_filename = tk.StringVar()              
        self.output_dir = tk.StringVar()
        self.output_file = tk.StringVar()

        self.__create_widgets()      

                
    def __create_widgets(self):  
        
        # Selection orientation      
        self.label_info = ttk.Label(self, text=self.info_select, font= 'Tahoma 14 bold' )
        self.label_info.grid(column=0,row=0, 
                             columnspan=4, 
                             padx=10, pady=10)    
              
        # Selected input file
        self.label_input_dir = tk.Label(self, text='Input file:')
        self.label_input_dir.grid(column=0, row=1, 
                                  stick=tk.E) 
        
        self.entry_file = ttk.Entry(self, textvariable=self.input_filename, font=('Tahoma',10)) 
        self.entry_file.grid(column=1, row=1, columnspan=2,
                            stick=tk.EW,
                            pady=10,
                            ipadx=5, ipady=5) 
        self.input_filename.trace_variable('w', self.onEntryInput)
        # self.entry_file.bind( '<Return>' , self.onEntryInput )  
        
        # Browse to select a file
        self.button_select  = ttk.Button(self, text='SELECT INPUT FILE', command=self.select_input_file )
        self.button_select.grid(column=3, row=1, 
                                stick=tk.EW,
                                ipadx=5, ipady=5)  
        
        # Orientation output      
        self.label_info_out = ttk.Label(self, text=self.info_select_output, font= 'Tahoma 14 bold' )
        self.label_info_out.grid(column=1, row=2, 
                                 columnspan=4, 
                                stick=tk.EW,
                                padx=10, pady=15)  
        
        # Output Directory
        # self.label_output_dir = tk.Label(self, 
        #                                  text='Output folder: ')
        # self.label_output_dir.grid(column=0, row=3, 
        #                            stick=tk.E)  
        
        # self.entry_output_dir = tk.Entry(self, 
        #                                  textvariable=self.output_dir,
        #                                  font=('Tahoma',10) )        
        # self.entry_output_dir.grid(column=1, row=3, 
        #                            columnspan=2,
        #                            stick=tk.EW,
        #                            ipadx=5, ipady=5,
        #                            pady=10)  
        
        # # Browse to select a file
        # self.button_select  = ttk.Button(self, 
        #                                  text='SELECT OUTPUT FOLDER', command=self.select_output_folder )
        # self.button_select.grid(column=3, row=3,
        #                         sticky=tk.EW,
        #                         ipadx=5, ipady=5)   
        
        # Output Directory        
        self.label_output_file = tk.Label(self, 
                                          text = 'Output filename: ')
        self.label_output_file.grid(column=0, row=4, 
                                    stick=tk.E)  
        
        
        self.entry_output_file = tk.Entry(self, 
                                          textvariable=self.output_file,
                                          font=('Tahoma',10))              
        self.entry_output_file.grid(column=1,row=4, 
                                    ipadx=5, ipady=5,
                                    stick=tk.EW)  
        
        # Button Convert
        self.button_convert= tk.Button(self,
                        text = 'CONVERT FILE',
                        command = lambda: 
                            convert_columns(
                                self.filename,
                                self.output_dir.get()+'/'+self.output_file.get())
                        )
        self.button_convert.grid(column=3,row=5, 
                                 ipadx=10, ipady=10,
                                 padx=10, pady=10)   
                
        
    def select_input_file(self):
        self.filetypes = ( ('Excel-XLS', '*.xls'), ('Excel-XLSX', '*.xlsx') )
        self.filename = fd.askopenfilename( 
                title = 'Select an Excel file',
                filetypes = self.filetypes  )
        self.input_dir, self.input_fname = os.path.split(self.filename)
        self.input_filename.set(self.input_dir + '/' + self.input_fname)
        
        
    # def select_output_folder(self):
    #     self.output_folder = fd.askdirectory( 
    #             title = '(optional) Select the output folder:'  )
    #     self.output_dir.set( self.output_folder )
        
    # def print_filename(self):
    #     self.output_dir.set(self.input_dir )
    #     self.output_file.set(self.input_fname )
    
    def onEntryInput(self, var, index, mode):
        self.output_dir.set(f'{self.input_dir}')
        self.output_file.set(f"{self.input_fname.split('.')[0]}_output.xlsx" )
        
                              
class Window(tk.Tk):    
    def __init__(self):
        super().__init__()                
        # Configure the root window
        self.title('Excel Converter')
        self.geometry('800x400+100+100' )
                
        self.__create_frames()
        
    def __create_frames(self):                
        # Frame: select input file
        frame_select = SelectFrame(self)
        frame_select.pack(expand=True, fill=tk.X)              
    
if __name__ == '__main__': 
    window = Window()
    window.mainloop()                 

