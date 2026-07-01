#This file holds classes that define and validate forms. Each class is one form.

class ParentRegistrationForm:
    def __init__(self, data):
        # data is request.form from Flask
        self.full_name = data.get('full_name', '').strip()
        self.phone_number = data.get('phone_number', '').strip()
        self.email = data.get('email','').strip()
        self.password = data.get('password','').strip()
        self.confrim_password = data.get('confrim_password','').strip()
        

    def validate(self):
        errors = []
        if not self.full_name:
            errors.append('Full name is required')
        if self.password != self.confrim_password:
            errors.append("password do not match")
        if not self.password:
            errors.append('Password is required')
        if not self.email:
            errors.append('email required')
        if not self.phone_number:
            errors.append('phone number required')
        return len(errors) == 0, errors

class ChildRegistrationForm: 
    def __init__(self,data):
        self.full_name = data.get('full_name', '')
        self.username = data.get('username', '')
        self.password = data.get('password', '')
        self.confrim_password = data.get('confrim_password', '')
        self.parent_phone = data.get('parent_phone', '')

    def validate(self):
        errors = []
        if self.password != self.confrim_password:
            errors.append("passwords do not match")
        if not self.full_name:
            errors.append('fullname required')
        if not self.password:
            errors.append('password required')
        if not self.username:
            errors.append('username required')
        if not self.parent_phone:
            errors.append('parent number required')
        return len(errors) == 0, errors

    

class LoginForm:
    def __init__(self, data):
        self.password = data.get('password', '')
        self.user_type = data.get('user_type', '')
        self.identifier = data.get('identifier', '')
        self.password = data.get('password', '')
        

    def validate(self):
        errors = []
        if self.user_type not in ['parent', 'child']:
            errors.append('Please select parent or child')
        if not self.identifier:
            errors.append('identifier required')
        if not self.password:
            errors.append('Password is required')
        return len(errors) == 0, errors
        
#The correct pattern for "check if a field is empty" is always just:
 #   if not self.field_name:
  #  errors.append('field is required') 
