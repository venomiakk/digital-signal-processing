# digital-signal-processing

```
#! CONTROLS
        # Signal tab buttons
        self.sig_generate.clicked.connect(self.generate_and_plot_signal)
        self.sig_save.clicked.connect(self.save_signal)
        self.sig_readfile.clicked.connect(self.load_signal_from_file)
        
        # Operations tab buttons
        self.op_generate_2.clicked.connect(self.generate_and_plot_signal1)
        self.op_save_2.clicked.connect(self.save_signal1)
        self.op_readfile_2.clicked.connect(self.load_signal1)
        
        self.op_generate_3.clicked.connect(self.generate_and_plot_signal2)
        self.op_save_3.clicked.connect(self.save_signal2)
        self.op_readfile_3.clicked.connect(self.load_signal2)
        
        self.op_executeop.clicked.connect(self.execute_operation)
        self.op_saveop.clicked.connect(self.save_operation_result)
        
        # Connect combo boxes to update enabled fields
        self.comboBoxSignals.currentIndexChanged.connect(self.update_enabled_fields)
        self.comboBoxSignals_2.currentIndexChanged.connect(self.update_enabled_fields_signal1)
        self.comboBoxSignals_3.currentIndexChanged.connect(self.update_enabled_fields_signal2)
        
        # Initialize plot frames
        self.setup_plot_frame()
        self.setup_operations_frames()
        
        self.retranslateUi(SignalProcessApp)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SignalProcessApp)
        
        #! CONTROLS
        # Initialize enabled fields
        self.update_enabled_fields()
        self.update_enabled_fields_signal1()
        self.update_enabled_fields_signal2()
        
        # Set default values
        self.set_default_values()

        # File tab buttons
        self.f_loadfile.clicked.connect(self.load_file_signal)
        self.f_refreshplot.clicked.connect(self.refresh_file_plot)
        
        # Make text areas read-only
        self.f_sigattr.setReadOnly(True)
        self.f_sigvalues.setReadOnly(True)
        
        # Initialize the file tab plot frame
        self.setup_file_frame()
```