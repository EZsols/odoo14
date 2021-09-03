from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


class HrEmployeeVisa(models.Model):
    _name = 'hr.employee.visa'
    _description = 'Employee Visa'
    _rec_name = 'seq_name'

    seq_name = fields.Char('Name', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee')
    state = fields.Selection([
        ('new', 'New'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
    ], string='Status', copy=False, index=True, default='new')
    category_id = fields.Many2one('hr.employee.visa.category', 'Category')
    approved_date = fields.Date(string='Approved Date')

    mobile_phone = fields.Char(related='employee_id.mobile_phone')
    company_id = fields.Many2one(related='employee_id.company_id')
    work_phone = fields.Char(related='employee_id.work_phone')
    work_email = fields.Char(related='employee_id.work_email')
    department_id = fields.Many2one(related='employee_id.department_id')
    coach_id = fields.Many2one(related='employee_id.coach_id')

    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', groups="hr.group_hr_user", related='employee_id.country_id')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], groups="hr.group_hr_user", related='employee_id.gender')

    place_of_birth = fields.Char('Place of Birth', groups="hr.group_hr_user", related='employee_id.place_of_birth')
    country_of_birth = fields.Many2one('res.country', string="Country of Birth", groups="hr.group_hr_user",
                                       related='employee_id.country_of_birth')
    birthday = fields.Date('Date of Birth', groups="hr.group_hr_user", related='employee_id.birthday')
    identification_id = fields.Char(string='Identification No', groups="hr.group_hr_user", related='employee_id.identification_id')
    passport_id = fields.Char('Passport No', groups="hr.group_hr_user", related='employee_id.passport_id')


    permit_no = fields.Char('Work Permit No', groups="hr.group_hr_user", related='employee_id.permit_no')
    visa_no = fields.Char('Visa No', groups="hr.group_hr_user", related='employee_id.visa_no')
    visa_expire = fields.Date('Visa Expire Date', groups="hr.group_hr_user", related='employee_id.visa_expire')

    embassy_id = fields.Many2one('hr.employee.visa.embassy', string='Embassy')
    commissioner_name = fields.Char(related='embassy_id.commissioner_name',)
    street = fields.Char(related='embassy_id.street', )
    street2 = fields.Char(related='embassy_id.street2', )
    city = fields.Char(related='embassy_id.city', )
    state_id = fields.Many2one(related='embassy_id.state_id',)
    embassy_country_id = fields.Many2one(related='embassy_id.country_id',)


    @api.model
    def create(self, vals):
        if vals.get('seq_name', ('New')) == ('New'):
            vals['seq_name'] = self.env['ir.sequence'].next_by_code('hr.employee.visa.sequence') or _('New')
        result = super(HrEmployeeVisa, self).create(vals)
        return result

    def action_approve(self):
        self.write({
            'state': 'approved',
            'approved_date': datetime.today(),
        })

    def action_refuse(self):
        self.write({
            'state': 'refused',
        })


class HrEmployeeVisaEmbassy(models.Model):
    _name = 'hr.employee.visa.embassy'
    _description = 'Employee Visa Embassy'
    _rec_name = 'name'

    name = fields.Char('Embassy Title')
    commissioner_name = fields.Char('Commissioner')
    street = fields.Char(readonly=False)
    street2 = fields.Char(readonly=False)
    city = fields.Char(readonly=False)
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')

class HrEmployeeVisaCategory(models.Model):
    _name = 'hr.employee.visa.category'
    _description = 'Employee Visa Category'
    _rec_name = 'name'

    name = fields.Char('Category')
    description = fields.Html('Description')

