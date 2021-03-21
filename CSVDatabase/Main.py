from PyQt5 import QtWidgets, QtGui, QtCore, Qt
import sys, os
import pandas as pD
import csv

class Database(QtWidgets.QMainWindow):
    
    def __init__(self, **kwargs):
        super(Database, self).__init__(**kwargs)
        
        self.__buttonWidth: int = 110
        self.__buttonHeight: int = 35
        self.__labels: str = ''
        self.__tableHeader_Labels = []
        self.__table_fontSize: int = 10
        
        self.setWindowIcon(QtGui.QIcon(r'CSVDatabase\CSV_Database_ICON.png'))
        self.setWindowTitle('CSV database')
        self.init_GUI()
        self.show()
        
    def init_GUI(self):
               
        database = QtWidgets.QWidget()
        database_Layout = QtWidgets.QVBoxLayout()

        database.setLayout(database_Layout)

        self.setCentralWidget(database)
        self.createUI(database_Layout)

    def createUI(self, database_Layout):
        
        #SAVE FILE
        self.saveFile_Button = QtWidgets.QPushButton('Save CSV')
        self.saveFile_Button.setFont(QtGui.QFont('Arial',10))
        self.saveFile_Button.setFixedSize(self.__buttonWidth,self.__buttonHeight)
        self.saveFile_Button.clicked.connect(self.saveFile)
        
        #OPEN FILE
        self.openFile_Button = QtWidgets.QPushButton('Open CSV')
        self.openFile_Button.setFont(QtGui.QFont('Arial',10))
        self.openFile_Button.setFixedSize(self.__buttonWidth,self.__buttonHeight)
        self.openFile_Button.clicked.connect(self.loadFile)
        
        #Table for DATA
        self.table_Database = QtWidgets.QTableWidget()
        self.table_Database.setStyleSheet('QHeaderView::section {background-color: #e3c378; border-left: 1px solid black; height: 20px; font-size: 15px}')
        self.table_Database.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.table_Database.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.table_FontSize = self.table_Database.font()

        #Table OPTIONS     
        self.newColumn_Label = QtWidgets.QLabel('Column name')
        self.newColumn_Label.setFont(QtGui.QFont('Arial',13))
        self.newColumn_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.newColumn_Label.setFixedSize(self.__buttonWidth,20)
        
        self.addNewColumnName_TEXT = QtWidgets.QLineEdit()
        self.addNewColumnName_TEXT.setFont(QtGui.QFont('Arial',13))
        self.addNewColumnName_TEXT.setAlignment(QtCore.Qt.AlignLeft)
        self.addNewColumnName_TEXT.setFixedSize(self.__buttonWidth,22)
        
        self.addNewColumn_Button = QtWidgets.QPushButton('Add new column')
        self.addNewColumn_Button.setFont(QtGui.QFont('Arial',10))
        self.addNewColumn_Button.setFixedSize(self.__buttonWidth,self.__buttonHeight)
        self.addNewColumn_Button.clicked.connect(self.addNewColumn)
        
        self.addNewRow_Button = QtWidgets.QPushButton('Add new row')
        self.addNewRow_Button.setFont(QtGui.QFont('Arial',10))
        self.addNewRow_Button.setFixedSize(self.__buttonWidth,self.__buttonHeight)
        self.addNewRow_Button.clicked.connect(self.addNewRow)

        self.removeRow_Button = QtWidgets.QPushButton('Remove row')
        self.removeRow_Button.setFont(QtGui.QFont('Arial',10))
        self.removeRow_Button.setFixedSize(self.__buttonWidth,self.__buttonHeight)
        self.removeRow_Button.clicked.connect(self.deleteSelectedRow)
   
        self.removeColumn_Button = QtWidgets.QPushButton('Remove column')
        self.removeColumn_Button.setFont(QtGui.QFont('Arial',10))
        self.removeColumn_Button.setFixedSize(self.__buttonWidth,self.__buttonHeight)
        self.removeColumn_Button.clicked.connect(self.deleteSelectedColumn)
           
        #Font size controls
        self.tableItem_FontSize_Label = QtWidgets.QLabel('Font size')
        self.tableItem_FontSize_Label.setFont(QtGui.QFont('Arial',10))
        self.tableItem_FontSize_Label.setAlignment(QtCore.Qt.AlignLeft)
        
        self.tableItem_FontSize_ADD = QtWidgets.QPushButton('+')
        self.tableItem_FontSize_ADD.setFont(QtGui.QFont('Arial',10))
        self.tableItem_FontSize_ADD.setFixedSize(30, self.__buttonHeight)
        self.tableItem_FontSize_ADD.clicked.connect(self.fontSize_UP)
        
        self.tableItem_FontSize= QtWidgets.QLabel(str(self.__table_fontSize))
        self.tableItem_FontSize.setFont(QtGui.QFont('Arial',13))
        self.tableItem_FontSize.setAlignment(QtCore.Qt.AlignCenter)
        self.tableItem_FontSize.setFixedSize(30, self.__buttonHeight)
           
        self.tableItem_FontSize_LOWER = QtWidgets.QPushButton('-')
        self.tableItem_FontSize_LOWER.setFont(QtGui.QFont('Arial',10))
        self.tableItem_FontSize_LOWER.setFixedSize(30, self.__buttonHeight)
        self.tableItem_FontSize_LOWER.clicked.connect(self.fontSize_DOWN)

        #Layouts    
        table_Layout = QtWidgets.QHBoxLayout()
        table_SideBar_Layout = QtWidgets.QVBoxLayout()
        fileControls_Layout = QtWidgets.QVBoxLayout()
        table_Control_Layout = QtWidgets.QVBoxLayout()
        table_SizeControls_Layout = QtWidgets.QHBoxLayout()
        
        font_Size_Layout = QtWidgets.QVBoxLayout()
        font_Size_Layout_Buttons = QtWidgets.QHBoxLayout()
        
        #Assign widgets
        fileControls_Layout.addWidget(self.saveFile_Button)
        fileControls_Layout.addWidget(self.openFile_Button)
        
        font_Size_Layout.addWidget(self.tableItem_FontSize_Label)
        font_Size_Layout_Buttons.addWidget(self.tableItem_FontSize_ADD)
        font_Size_Layout_Buttons.addWidget(self.tableItem_FontSize)
        font_Size_Layout_Buttons.addWidget(self.tableItem_FontSize_LOWER)

        font_Size_Layout.addLayout(font_Size_Layout_Buttons)
        table_SizeControls_Layout.addLayout(font_Size_Layout)
        table_SizeControls_Layout.setAlignment(QtCore.Qt.AlignLeft)

        table_Control_Layout.addWidget(self.newColumn_Label)
        table_Control_Layout.addWidget(self.addNewColumnName_TEXT)
        table_Control_Layout.addWidget(self.addNewColumn_Button)
        table_Control_Layout.addWidget(self.addNewRow_Button)
        table_Control_Layout.addWidget(self.removeColumn_Button)
        table_Control_Layout.addWidget(self.removeRow_Button)

        #Groups
        self.fileGroup = QtWidgets.QGroupBox('File options')
        self.tableControls = QtWidgets.QGroupBox('Tabel')
        self.databaseOptions = QtWidgets.QGroupBox('Tabel options')
        
        self.fileGroup.setFixedWidth(self.__buttonWidth + 20)
        self.tableControls.setFixedWidth(self.__buttonWidth + 20)
        self.databaseOptions.setFixedWidth(self.__buttonWidth + 20)
          
        #Initialize Groups
        self.fileGroup.setLayout(fileControls_Layout)
        self.tableControls.setLayout(table_Control_Layout)
        self.databaseOptions.setLayout(table_SizeControls_Layout)
        
        #Initialize layout widgets
        table_SideBar_Layout.addWidget(self.fileGroup)
        table_SideBar_Layout.addWidget(self.tableControls)
        table_SideBar_Layout.addStretch()
        table_SideBar_Layout.addWidget(self.databaseOptions)

        table_Layout.addWidget(self.table_Database)
        self.table_Database.horizontalHeader().sectionDoubleClicked.connect(self.renameColumnHeader)
        
        table_Layout.addLayout(table_SideBar_Layout)
        database_Layout.addLayout(table_Layout)
    
    def deleteSelectedRow(self):
        
        self.selectedRows  = self.table_Database.selectedIndexes()
        if self.selectedRows :
            rows = set(i.row() for i in self.selectedRows )
        else:
            rows = [self.table_Database.rowCount()-1]
            
        for row in sorted(rows,reverse=True):
            self.table_Database.removeRow(row)
            
    def deleteSelectedColumn(self):
        self.selectedColumn = self.table_Database.selectedIndexes()
        if self.selectedColumn :
            columns = set(i.column() for i in self.selectedColumn )
        else:
            columns = [self.table_Database.columnCount()-1]
            
        for column in sorted(columns,reverse=True):
            self.table_Database.removeColumn(column)
                     
            if len(self.__tableHeader_Labels) != 0:
                del self.__tableHeader_Labels[column]

    def renameColumnHeader(self,index):
      
        self.oldColumnHeader = self.table_Database.horizontalHeaderItem(index).text()
        self.newColumnHeader, ok = QtWidgets.QInputDialog.getText(self,
                                                      'Column header %d' % index,
                                                      'New column header name:',
                                                       QtWidgets.QLineEdit.Normal,
                                                       self.oldColumnHeader)
        if ok:
            self.table_Database.horizontalHeaderItem(index).setText(self.newColumnHeader)
            self.__tableHeader_Labels[index] = self.newColumnHeader
     
    def loadFile(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QMainWindow(),'Open CSV file',os.getenv('HOME'),'CSV(*.csv)')
       
        if filePath[0] != '':
            with open(filePath[0]) as csv_file:
                try:
                    my_file = pD.read_csv(csv_file)
  
                    self.table_Database.setRowCount(my_file.shape[0])
                    self.table_Database.setColumnCount(my_file.shape[1])
                    self.table_Database.setHorizontalHeaderLabels(my_file.keys())
                    
                    for i in my_file.keys():
                        self.__tableHeader_Labels.append(i)
                        print(self.__tableHeader_Labels)
                     
                    print(my_file.keys())
                    for x, key in enumerate(my_file.keys()):  
                        for y, value in enumerate(my_file[key]):    
                            self.table_Database.setItem(y,x,QtWidgets.QTableWidgetItem(str(value)))
                            print(value)
                            
                except:
                    self.fileError_message = QtWidgets.QErrorMessage()
                    self.fileError_message.showMessage('CSV file is damaged or empty, please open CSV file that contains data')

    def saveFile(self):
        fileName = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QMainWindow(),'Save CSV file as',os.getenv('HOME'),'CSV(*.csv)')
        print(fileName)
        if fileName[0] != '':
            with open(fileName[0],'w') as file:
                csvFile = csv.writer(file)

                try:
                    columnHeaders = []
                    for currentHeader in range (self.table_Database.columnCount()):
                        columnHeaders.append(str(self.table_Database.horizontalHeaderItem(currentHeader).text()))
                    csvFile.writerow(columnHeaders)

                    for row in range(self.table_Database.rowCount()):
                        row_data = []
                        for column in range(self.table_Database.columnCount()):
                            dataToSave = self.table_Database.item(row, column)
                            if dataToSave is not None:
                                row_data.append(dataToSave.text())
                            else:
                                row_data.append('')
                        csvFile.writerow(row_data)
                  
                except: 
                    self.fileError_message = QtWidgets.QErrorMessage()
                    self.fileError_message.showMessage("Warning ! CSV file can't be saved, table is missing data or contains unreadable symbols")

    def addNewRow(self):
        self.tableRow =  self.table_Database.rowCount()   
        self.table_Database.setRowCount(self.tableRow + 1)
        self.table_Database.setItem(self.tableRow,0, QtWidgets.QTableWidgetItem() )
        
    def addNewColumn(self):
        self.error_message = QtWidgets.QErrorMessage()
        if self.addNewColumnName_TEXT.text() == '':
            self.error_message.showMessage('Please add column header name to create new column')
        else:
            self.tableColumn =  self.table_Database.columnCount()         
            self.table_Database.setColumnCount(self.tableColumn + 1)
            self.table_Database.setItem(0,self.tableColumn,QtWidgets.QTableWidgetItem())
   
            self.__tableHeader_Labels.append(self.addNewColumnName_TEXT.text())
            self.table_Database.setHorizontalHeaderLabels(self.__tableHeader_Labels)
            self.addNewColumnName_TEXT.clear()
   
    def fontSize_UP(self):
        if self.__table_fontSize != 9 and  self.__table_fontSize < 30:
            self.__table_fontSize += 1
            self.tableItem_FontSize.setText(str(self.__table_fontSize))
            self.table_FontSize.setPointSize(int(self.__table_fontSize))
            self.table_Database.setFont(self.table_FontSize)
            
    def fontSize_DOWN(self):
        if self.__table_fontSize != 10:
            self.__table_fontSize -= 1
            self.tableItem_FontSize.setText(str(self.__table_fontSize))
            self.table_FontSize.setPointSize(int(self.__table_fontSize))
            self.table_Database.setFont(self.table_FontSize)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    appWindow = Database()
    sys.exit(app.exec_())