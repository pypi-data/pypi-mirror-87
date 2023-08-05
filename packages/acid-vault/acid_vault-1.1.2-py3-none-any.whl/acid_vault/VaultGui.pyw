###############################################################################
# Acid Vault                                                                  #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU Affero General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Affero General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

from version import *
try:
    import datetime
    from distutils.version import LooseVersion
    import json
    import time
    import pickle
    import os
    import tkinter
    import tkinter.messagebox
    import tkinter.filedialog
    import tkinter.ttk
    import urllib.request

    import constants
    import legacy_load
    import ssh
    import steganography
    from vault import Vault, VaultError
    import widgets
except ImportError as err:
    tkinter.messagebox.showerror('Failed to import', err)
    raise

class GUI():
    """GUI to handle a password vault."""
    def __init__(self, master):
        self.startup_ok = False
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.onclose)
        self.title = 'PyVault'
        self.master.title(self.title)
        self.vault = None
        self.ssh_config = {}
        self.file_config = {}
        self.last_update = False
        
        top = tkinter.Frame(master)
        top.pack(side='top', fill=tkinter.X)
        self.passbox = PasswordBox(master)
        self.passbox.dirty.trace('w', self.dirty)
        self.passbox.pack(side='top', fill=tkinter.BOTH, expand=1)
        self.status = widgets.StatusBar(master, relief=tkinter.RAISED)
        self.status.pack(side='top', fill=tkinter.X)
        bottom = tkinter.Frame(master)
        bottom.pack(side='top', fill=tkinter.X)

        self.password = tkinter.StringVar()
        self._password = None
        password = widgets.LabelEntry(top,
                                      label='Password',
                                      show='*',
                                      textvariable=self.password)

        password.bind('<Return>', self.on_return_key)
        # Activity sensor.
        timer = widgets.Timer(self.master, self.lock, 5000*60)
        master.bind_all('<Enter>', timer.reset)

        # Buttons.
        save_pass = widgets.Box(
            top, 'Button', text='Save passwords', command=self.save_encrypted)
        get_pass = widgets.Box(
            top, 'Button', text='Load passwords', command=self.load_encrypted)
        self.lock_btn = widgets.Box(top,
                                    'Button',
                                    text='Unlock',
                                    command=self.toggle_lock,
                                    state=tkinter.DISABLED)
        add_pass = tkinter.Button(
            bottom, command=self.add_password, text='Add Password')

        # Checkboxes
        
        # Option menues
        self.file_location = tkinter.StringVar()
        self.file_location.set('Local')
        file_location = tkinter.OptionMenu(
            top, self.file_location, 'Local', 'Remote')
        file_location.configure(width=15)

        # Menu bar
        menubar = tkinter.Menu(master, tearoff=0)
        filemenu = tkinter.Menu(menubar, tearoff=0)
        helpmenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Setup SSH', command=self.setup_ssh)
        filemenu.add_command(label='Setup Files', command=self.setup_files)
        filemenu.add_command(
            label='Save cleartext',
            command=lambda *args,**kwargs : self.ask_for_file(
                'save_clear', 'w'))
        filemenu.add_command(
            label='Load cleartext',
            command=lambda *args,**kwargs : self.ask_for_file(
                'load_clear', 'r'))
        filemenu.add_command(
            label='Save encrypted',
            command=lambda *args,**kwargs : self.ask_for_file(
                'save_encrypted', 'wb'))
        filemenu.add_command(
            label='Load encrypted',
            command=lambda *args,**kwargs : self.ask_for_file(
                'load_encrypted', 'rb'))
        helpmenu.add_command(
            label='About',
            command=lambda:widgets.About(self.master, 'About'))
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label='Help', menu=helpmenu)
        master.config(menu=menubar)

        # Pack it all up
        password.pack(side='left')
        get_pass.pack(side='left', fill=tkinter.Y)
        save_pass.pack(side='left', fill=tkinter.Y)
        self.lock_btn.pack(side='left', fill=tkinter.Y)
        file_location.pack(side='right', fill=tkinter.Y)
        add_pass.pack()
        self.onstart()
        password.focus_set()
        self.startup_ok = True
        
    def onclose(self):
        """Runs on GUI close to save settings."""
        # Dont overwrite settings with empty values if startup failed.
        if not self.startup_ok:return
        if self.dirty() and not tkinter.messagebox.askokcancel(
            'Quit without save?', 'Unsaved passwords exists, quit anyway?'):
            return
        try:
            ssh_config = self.ssh_config
            file_config = self.file_config
            # Clearing SSH-Password if set
            if ssh_config:
                ssh_config['password'] = ''
            if file_config and file_config.get('clear_on_exit'):
                file_config = {}
            obj = {'attributes': {'ssh_config': ssh_config,
                                  'file_config': file_config,
                                  'last_update': self.last_update},
                   'widgets': {'file_location': self.file_location.get()},
                   'version': '1.0.0'}
            with open(os.path.join(constants.data_dir(), '.vault'), 'wb') as fh:
                pickle.dump(obj, fh)
        except Exception as err:
            print(err)
        finally:
            self.master.destroy()

    def onstart(self):
        """Runs on GUI start to load saved settings."""
        try:
            with open(os.path.join(constants.data_dir(), '.vault'), 'rb') as fh:
                obj = pickle.load(fh)
            if not obj.get('version') == '1.0.0':
                obj = legacy_load.legacy_load(obj)
            for key, value in obj['widgets'].items():
                try:
                    getattr(self, key).set(value)
                except Exception as err:
                    print(err)
            for key, value in obj['attributes'].items():
                setattr(self, key, value)
            now = datetime.datetime.now()
            if not self.last_update or now - self.last_update > datetime.timedelta(days=7):
                self.last_update = now
                if self.check_version('acid_vault') != __version__:
                    self.status.set('New version avaliable at pypi', 'green')

        except Exception as err:
            print(err)

    def on_return_key(self, *event):
        if self.vault and self.vault.locked:
            self.update_password_box()
        else:
            self.load_encrypted()

    def ask_for_file(self, call_type, mode):
        initialdir = os.path.expanduser('~')
        initialfile = time.strftime('%Y%m%d-%H%M%S')
        if self.file_config.get('use_steganography'):
            filetypes = (('Image file', '*.png'), ('All files', '*.*'))
            defaultextension='.png'
        else:
            filetypes = (('Text file', '*.txt'), ('All files', '*.*'))
            defaultextension='.txt'
        kwargs = {'master': self.master,
                  'title': 'Filename',
                  'defaultextension': defaultextension,
                  'filetypes': filetypes,
                  'initialdir': initialdir,
                  'initialfile': initialfile}
        if 'save' in call_type:
            path = tkinter.filedialog.asksaveasfilename(**kwargs)
        elif 'load' in call_type:
            path = tkinter.filedialog.askopenfilename(**kwargs)
        if not path: return
        try:
            with open(path, mode) as fh:
                getattr(self, call_type)(fh)
        except OSError:
            self.status.set(f'Unable to open file: {path}', color='red')

    def steganography_load(self, fh):
        """Load hidden data from a file."""
        self.status.set('Loading hidden data')
        data = steganography.read(fh, self.file_config['original_file'])
        self.vault = Vault()
        self.vault.load_data(data)
        self.status.set('Hidden data loaded')

    def steganography_save(self, fh):
        """Save data hidden in a file."""
        self.status.set('Hiding data')
        data = self.vault.save_data()
        steganography.write(fh, self.file_config['original_file'], data)
        self.status.set('Data hidden')

    def load_encrypted(self, fh=False):
        """Get and unlock passwords from vault."""
        def load_passwords(fh):
            if not fh:
                return
            if self.file_config.get('use_steganography'):
                self.steganography_load(fh)
            else:
                self.vault = Vault(fh)
        if not (fh or self.verify()):
            return
        location = fh.name if fh else self.file_config['file_location']
        if fh:
            self.status.set(f'Loading passwords from: {location}')
            load_passwords(fh)
        elif self.file_location.get() == 'Local':
            self.status.set(f'Getting local passwords at: {location}')
            self.make_dirs()
            with open(location, 'rb') as fh:
                load_passwords(fh)
        elif self.file_location.get() == 'Remote':
            self.status.set(f'Getting remote passwords at: {location}')
            try:
                with ssh.RemoteFile(self.ssh_config,
                                    location,
                                    constants.data_dir(), 'r') as fh:
                    load_passwords(fh)
            except Exception as err:
                self.status.set(err, color='red')
                return
        self.status.set('Passwords successfully recieved')
        self.update_password_box()

    def update_password_box(self):
        """Load passwords in to GUI."""
        self.status.set('Updating password box')
        self.passbox.clear()
        self._password = self.password.get()
        self.status.set('Unlocking vault')
        self.vault.unlock(self._password)
        self.lock_btn.config(text='Lock')
        self.lock_btn.config(state=tkinter.NORMAL)
        for password in sorted(self.vault.get_objects()):
            self.passbox.add(password)
        self.passbox.dirty.set(False)
        self.status.set('Passwords updated')

    def save_encrypted(self, fh=False):
        """Save password in to file."""
        def save_passwords(fh):
            if self.file_config.get('use_steganography'):
                self.steganography_save(fh)
            else:
                self.vault.save_file(fh)
            
        self.status.set('Saving passwords')
        if not (fh or self.verify()):
            return
        if not self.vault:
            self.vault = Vault(self.password.get())
        objects = [self.passbox.item(x, 'values') for x in
                   self.passbox.get_children()]
        self.vault.set_objects(objects)
        self.vault.lock(self._password)
        location = fh.name if fh else self.file_config['file_location']
        if fh:
            save_passwords(fh)
            self.status.set(f'Saving passwords at: {location}')
        elif self.file_location.get() == 'Local':
            self.status.set(f'Saving passwords localy at: {location}')
            self.make_dirs()
            with open(location, 'wb') as fh:
                save_passwords(fh)
                
        elif self.file_location.get() == 'Remote':
            self.status.set(f'Saving passwords remotly at: {location}')
            with ssh.RemoteFile(self.ssh_config,
                                location,
                                constants.data_dir(), 'w') as fh:
                save_passwords(fh)
        
        self.vault.unlock(self._password)
        self.passbox.dirty.set(False)
        self.status.set('Passwords saved')

    def save_clear(self, fh):
        try:
            self.vault.save_clear(fh)
        except VaultError as err:
            self.status.set(err, color='red')

    def load_clear(self):
        if self.passbox.dirty.get():
            self.status.set('Save current passwords first', color='red')
            return
        if not self.vault:
            self.vault = Vault()
        try:
            self.vault.load_clear(fh)
        except VaultError as err:
            self.status.set(err, color='red')
        else:
            self.update_password_box()

    def check_version(self, name):
        pypi_url = f'https://pypi.org/pypi/{name}/json'
        response = urllib.request.urlopen(pypi_url, timeout=5).read().decode()
        latest_version = max(LooseVersion(s) for s in
                             json.loads(response)['releases'].keys())
        return latest_version

    def verify(self):
        """Verify mandatory information."""
        if not self.password.get():
            tkinter.messagebox.showerror('Set Password',
                                         'Password has to be set')
            return

        if self.file_location.get() == 'Local':
            if not self.file_config['file_location']:
                tkinter.messagebox.showerror('Set Filepath',
                                             'Local Filepath has to be set')
                return
        elif self.file_location.get() == 'Remote':
            # Add validation here
            return True
        else:
            return
        return True

    def setup_files(self):
        """Setup files throught dialog."""
        result = widgets.SetupFiles(self.master,
                                  'File Config',
                                  self.file_config).result
        if result:
            self.file_config = result

    def add_password(self):
        """Add a new password to password list."""
        self.passbox.add()

    def setup_ssh(self):
        """Setup ssh settings throught a dialog."""
        result = widgets.SetupSSH(self.master,
                                  'SSH Config',
                                  self.ssh_config).result
        if result:
            self.ssh_config = result

    def make_dirs(self):
        """Create directory to contain files if it does not exist."""
        dirname = os.path.dirname(self.file_config['file_location'])
        if dirname:
            os.makedirs(dirname, exist_ok=True)

    def lock(self):
        """Lock vault, and clear local password list."""
        self.status.set('Locking vault')
        if self.vault and not self.vault.locked:
            self.vault.lock(self._password)
            self.lock_btn.config(text='Unlock')
        self._password = None
        self.password.set('')
        self.passbox.clear()
        self.status.set('Vault locked')
        
    def toggle_lock(self):
        """Toggle lock and unlock of vault."""
        if self.password.get() and self.vault and self.vault.locked:
            self.update_password_box()          
        elif self.vault and self._password:
            self.lock()

    def dirty(self, *args, **kwargs):
        dirty = ' *' if self.passbox.dirty.get() else ''
        self.master.title(self.title + dirty)
        return bool(dirty)


class PasswordBox(tkinter.ttk.Treeview):
    """Class to display password list."""
    def __init__(self, master):
        columns = ('System', 'User Name', 'Password', 'Notes')
        self.f = tkinter.Frame(master)
        super().__init__(self.f,
                         columns=columns,
                         displaycolumns=('System', 'User Name'),
                         show='headings')
        super().pack(fill=tkinter.BOTH, expand=1, side='left')
        sb = tkinter.ttk.Scrollbar(
            self.f, orient="vertical", command=self.yview)
        sb.pack(side='right', fill=tkinter.Y)
        self.configure(yscrollcommand=sb.set)
        for name in columns:
            self.heading(name, text=name)
        self.bind('<ButtonPress-1>', self.on_click)
        self.dirty = tkinter.BooleanVar()
        self.dirty.set(False)

    def pack(self, *args, **kwargs):
        self.f.pack(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.f.place(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.f.grid(*args, **kwargs)
        
    def clear(self):
        """Remove all unlocked passwords from the list."""
        children = self.get_children()
        self.dirty.set(False)
        if children:
            self.delete(*children)

    def add(self, password=None):
        """Add new password to password list."""
        password = password or widgets.AddPassword(self.master).result
        if not password: return
        for index, iid in enumerate(self.get_children()):
            if self.set(iid, 'System').lower() > password[0].lower():
                self.insert('', index, values=password)
                break
        else:
            self.insert('', 'end', values=password)
        self.dirty.set(True)

    def edit(self, iid):
        """Edit password."""
        if not iid: return
        values = self.item(iid, 'values')
        result = widgets.AddPassword(self.master, 'Password', values).result
        # We got a result and atleast one field has changed
        if result and [x for x in zip(values, result) if x[0] != x[1]]:
            self.delete(iid)
            self.add(result)
        
    def on_click(self, event):
        """Open Edit dialog on click."""
        region = self.identify("region", event.x, event.y)
        if region == 'heading':
            return
        self.edit(self.identify_row(event.y))
 
tk = tkinter.Tk()
GUI(tk)
tk.mainloop()
