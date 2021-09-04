from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


class HrEmployeeVisa(models.Model):
    _name = 'hr.employee.visa'
    _description = 'Employee Visa'
    _rec_name = 'seq_name'

    seq_name = fields.Char('Name', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    user_id = fields.Many2one(related='employee_id.user_id')
    surname = fields.Char(required=True,index=True)
    other_name = fields.Char(required=True, index=True)
    travel_passport_id = fields.Char('Passport No', required=True)
    travel_country_id = fields.Many2one(
        'res.country', 'Country of Travel', required=True)
    travel_date = fields.Date('Travel Date', required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
    ], string='Status', copy=False, index=True, default='new')
    category_id = fields.Many2one('hr.employee.visa.category', 'Category', required=True)
    job_id = fields.Many2one(related='employee_id.job_id')
    registration_number = fields.Char(related='employee_id.registration_number')
    first_contract_date = fields.Date(related='employee_id.first_contract_date')
    approved_date = fields.Date(string='Approved Date')
    approver_id = fields.Many2one('hr.employee', string='Approver', required=True)
    company = fields.Many2one('res.company', string='Company', required=True)
    approver_name = fields.Char(related='approver_id.name')
    approver_email = fields.Char(related='approver_id.work_email')



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

    embassy_id = fields.Many2one('hr.employee.visa.embassy', string='Embassy', required=True)
    commissioner_name = fields.Char(related='embassy_id.commissioner_name',)
    street = fields.Char(related='embassy_id.street', )
    street2 = fields.Char(related='embassy_id.street2', )
    city = fields.Char(related='embassy_id.city', )
    state_id = fields.Many2one(related='embassy_id.state_id',)
    embassy_country_id = fields.Many2one(related='embassy_id.country_id',)

    address = fields.Text(compute='get_partner_address')
    def get_partner_address(self):
        for rec in self:
            rec.address = "{street} {street2}, \n {city} {state}, \n{country}".format(
                street=rec.street,
                street2=rec.street2,
                city=rec.city,
                state=rec.state_id.name,
                country=rec.embassy_country_id.name
                )


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

    def action_print(self):
        # active_ids = self.env.context.get('active_ids', [])
        # datas = {
        #     'ids': active_ids,
        #     'model': 'report.model',
        #     'form': self.read()[0]
        # }
        return self.env.ref('fl_employee_visa.intro_letter').report_action(self)

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

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    registration_number = fields.Char()
    first_contract_date = fields.Date()

