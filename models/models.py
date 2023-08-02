# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from odoo.exceptions import ValidationError
from decimal import Decimal

class technology(models.Model):
    _name = 'shoe.technologies'

    name = fields.Char(string = "Solution Name", required = True)
    tags = fields.Many2many('shoe.tags.technologies',string = "Tag")
    functionalities = fields.Many2many('shoe.functionalities',string = "Functionalities")
    supplier = fields.Many2one('shoe.suppliers',string = "Supplier")
    ratings = fields.Many2many('shoe.ratings',string = "Ratings")
    short_description = fields.Char(string = "Description")
    # Questions

    rating_stars = fields.Integer(string = "Rating")
    comments = fields.Integer(string = "Comments")

    # Costs
    total_yearly_cost = fields.Float(string = "Total Yearly Cost")
    upfront_cost = fields.Float(string = "Upfront Cost", required = True)
    recurrent_cost = fields.Float(string = "Recurrent Cost", required = True)

    period_cost = fields.Selection([
        ('month', 'Monthly'),
        ('year', 'Yearly')
    ], string = "Period", default = "month", required = True)

    
    # Cost Scheme
    cost_scheme = fields.Selection([
        ('freemium', 'Freemium'),
        ('subscription', 'Tiered Subscription'),
        ('usage', 'Usage-based'),
        ('one', 'One-time')
    ], string = "Cost Scheme", default = "subscription", required = True)

    # User friendliness
    manuals = fields.Boolean(string = "Do you provide digital or written manuals with the solution?")
    help = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
        ('na', 'Not applicable')
    ], string = "Does your software provide help menus for the user?", default = "no", required  = True)

    # Deployment
    deployment = fields.Selection([
        ('full', 'Full deployment'),
        ('assisted', 'Assisted'),
        ('solo', 'No assistance')
    ], string = "Type of deployment provided to the customer", default = "full", required = True)

    # Training
    training_free = fields.Boolean(string = "Do you provide training for free?")
    hours_free = fields.Float(string = "Hours for free")
    
    training_cost = fields.Boolean(string = "Do you provide training under a cost?")
    cost_training = fields.Float(string = "Cost of training to given hours")
    hours_cost = fields.Float(string = "Hours for the specified cost")

    # Testing
    test = fields.Boolean(string = "Do you provide any trails?")
    test_free = fields.Boolean(string = "Is it free?")
    test_limit = fields.Boolean(string = "Is it for unlimited time?")
    cost_trail = fields.Float(string = "Cost of trail")
    deepness_trail = fields.Float(string = "Percentage of base functionalities available in trail?")
    lenght_trail = fields.Integer(string = "Days of trail")

    # Skills
    skills_use = fields.Many2many('shoe.skills', string = "Skills required to use", relation = 'skill_use', column1='solution', column2='use')
    skills_configure = fields.Many2many('shoe.skills', string = "Skills required to configure", relation = 'skill_configure', column1='solution', column2='configure')

    # Configurability
    configurability_level = fields.Selection([
        ('fixed','Not able for user to configure the solution'),
        ('limited','User can modify specific parts of the solution'),
        ('ample','User can modify the majority of the solution'),
        ('full','User can completely configure the solution')
    ], string = "Configurability Level", required = True)

    # Customization
    customization_level = fields.Selection([
        ('fixed','One solution no customization available'),
        ('limited', 'Limited customization (i.e. add fields or custom views)'),
        ('ample', 'Customization able to adapt to customer needs'),
        ('full', 'Full customized solution')
    ], string = "Customization Level", required = True)
    customization_cost = fields.Float(string = "Average cost of customization")

    # Support
    support_presence = fields.Boolean(string = "Do you provide ongoing support?")
    support_free = fields.Boolean(string = "Is this support included?")
    support_availability = fields.Selection([
        ('all', '24/7'),
        ('working', 'Working hours'),
        ('none', 'None')
    ], string = "Support Availability (select closest)")
    support_cost = fields.Float(string = "Average yearly cost of support")

    @api.onchange('recurrent_cost')
    def update_total_recurrent(self):
        
        if self.period_cost == 'year':
            factor = 1
        else: 
            factor = 12
        self.total_yearly_cost = self.recurrent_cost * factor


    def action_view_stars(self):
        pass

    def action_view_comments(self):
        pass

    def add_comment(self):
        pass

class technology_options(models.Model):
    _name = 'shoe.technologies.options'

    name = fields.Char(string ='Name')
    solution = fields.Many2one('shoe.technologies', string = "Solution")
    eval_functionality = fields.Float(string = "Technical")
    eval_characteristics = fields.Float(string = "General")
    eval_feedback = fields.Float(string = "Stars")
    favorite = fields.Boolean(string = "Favorites")
    notes = fields.Text(string = "Notes")
    eval_cost = fields.Float(string = "Cost")
    eval_cost_scheme = fields.Float(string = "Cost Scheme")
    eval_user_friend = fields.Float(string = "UX")
    eval_testing = fields.Float(string = "Testing")
    eval_training = fields.Float(string = "Training")
    eval_deployment = fields.Float(string= "Deploy")
    eval_customization = fields.Float(string = "Custom")
    eval_configurability = fields.Float(string = "Config")
    eval_support = fields.Float(string = "Support")

class tagstechnology(models.Model):
    _name = 'shoe.tags.technologies'
    name = fields.Char(string = "Tag Name", required = True)
    functionalities = fields.Many2many('shoe.functionalities',string = "Functionalities")

    @api.onchange('functionalities')
    def update_functionality_tag(self):
        if self.functionalities:
            match = self.env['shoe.functionalities'].search([])
            for element in match:
                element.tags = [(3, self.id, 0)]
            for element in self.functionalities:
                element.tags = [(4, self.id)]
            

class functionalities(models.Model):
    _name = 'shoe.functionalities'
    name = fields.Char(string = "Functionality", required = True)
    tags = fields.Many2many('shoe.tags.technologies',string = "Tag")

class weightedfunctionalities(models.Model):
    _name = 'shoe.weighted.functionalities'
    name = fields.Char(string = "Functionality", required = True)
    functionalities = fields.Many2one('shoe.functionalities',string = "Functionalities")
    weight = fields.Integer(string = "Weight (1-10)")
    searching = fields.Many2one('shoe.searches', string = "Searches")

class skills(models.Model):
    _name = 'shoe.skills'
    name = fields.Char(string = "Skill", required = True)
    description = fields.Text(string = "Description", required = True)

class smes(models.Model):
    _name = 'shoe.smes'
    name = fields.Char(string = "Company Name", required = True)
    code = fields.Char(string = "Code")

    # Company's Contact Information
    website = fields.Char(string ="Web Site", required = True)
    phone_number = fields.Char(string = "Company's Number", required = True)
    
    # Location
    country = fields.Many2one('res.country',string = "Country", required = True)
    state = fields.Many2one('res.country.state', string="State", store=True)
    city = fields.Char(string = "City")

    @api.onchange('country')
    def set_values_to(self):
        if self.country:
            ids = self.env['res.country.state'].search([('country_id', '=', self.country.id)])
            return {
                'domain': {'state': [('id', 'in', ids.ids)],}
            }

    def action_view_comments(self):
        pass
    
    def action_view_implementations(self):
        pass

    # Contact Information
    contact = fields.Char(string = "Name of Contact", required = True)
    phone_number_contact = fields.Char(string = "Contact's Number")
    email_contact = fields.Char(string = "Email")

    # Stats
    comments = fields.Integer(string = "Feedbacks")
    implementations = fields.Integer(string = "Implementations")

    # General Questions
    num_employees = fields.Integer(string = "Approx. # of employees", required = True)
    company_industry = fields.Selection([
        ('aerospace', 'Aerospace'),
        ('agriculture', 'Agriculture'),
        ('architecture', 'Architecture'),
        ('art_and_design', 'Art and Design'),
        ('automotive', 'Automotive'),
        ('biotechnology', 'Biotechnology'),
        ('construction', 'Construction'),
        ('consulting', 'Consulting'),
        ('education', 'Education'),
        ('e-commerce', 'E-commerce'),
        ('energy', 'Energy'),
        ('entertainment', 'Entertainment'),
        ('environmental', 'Environmental'),
        ('fashion', 'Fashion'),
        ('finance', 'Finance'),
        ('food_and_beverage', 'Food and Beverage'),
        ('gaming', 'Gaming'),
        ('healthcare', 'Healthcare'),
        ('hospitality', 'Hospitality'),
        ('insurance', 'Insurance'),
        ('logistics', 'Logistics'),
        ('manufacturing', 'Manufacturing'),
        ('media', 'Media'),
        ('mining', 'Mining'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('real_estate', 'Real Estate'),
        ('retail', 'Retail'),
        ('sports', 'Sports'),
        ('technology', 'Technology'),
        ('telecommunications', 'Telecommunications'),
        ('transportation', 'Transportation'),
        ('travel_and_tourism', 'Travel and Tourism'),
        ('other', 'Other'),
    ], string = "Industry", required = True)


    # Skills Questions
    skills = fields.Many2many('shoe.skills', string = "Which skills does your company has?")
    experience = fields.Boolean(string = "Do you have any previous experience with digital solution deployment?", required = True)
    team_digital = fields.Boolean(string = "Do you have a designated team for digital implementation?")
    technological_saavy = fields.Selection([
        ('highest','Highly Saavy (Developers, Configurators)'),
        ('high', 'Saavy (Native Digital Users)'),
        ('medium', 'OK (Proficient Computer User)'),
        ('low','Low (User with difficulties)'),
        ('lowest','Lacking (No CPU use at all)')
    ], string = "Indicate how technological saavy is your team in average", required = True)
    coding = fields.Boolean(string = "Do you have anyone with coding skills?")

    # Searches
    searches = fields.Many2many('shoe.searches', string = "Searches")

    # User
    user = fields.Many2one('res.users', string = "User", required = True)

    @api.model
    def create(self, vals):
        num_sme= self.env['shoe.smes'].search([('name', '!=', '')])
        if num_sme:
            num = len(num_sme) +1
        else:
            num = 1
        num = "{:04d}".format(num)
        sme = super(smes, self).create(vals)
        sme.code = str(num)
        return sme

class search(models.Model):
    _name = "shoe.searches"

    name = fields.Char(string = "Title", required = True)
    code = fields.Char(string = "Code")
    date = fields.Date(string = "Date of Creation")

    tags = fields.Many2many('shoe.tags.technologies', string = "Technologies")
    functionalities = fields.Many2many('shoe.functionalities',string = "Functionalities")
    weighted_functionalities = fields.Many2many('shoe.weighted.functionalities',string = "Wishlist")
    upfront_budget_max = fields.Float(string = "Upfront Budget", required = True)
    yearly_budget_max = fields.Float(string = "Yearly Budget", required = True)
    total_budget_max = fields.Float(string = "Total Budget", required = True)
    sme = fields.Many2one('shoe.smes', string = "Company")
    time = fields.Char(string = "Time of Creation")


    skills = fields.Many2many('shoe.skills', string = "Skills")
    solutions = fields.Many2many('shoe.technologies.options', string = "Solutions")
    chosen = fields.Many2one('shoe.technologies', string = "Chosen Solution")

    tailored = fields.Selection([
        ('generic', 'No need for tailored solution'),
        ('some', 'Some tailoring required (able to adapt process to solution)'),
        ('tailored', 'Need for detailed tailored solution (adapt to MY process)')
    ], string = "Need for tailored solution", default = "generic", required = True)
    updates = fields.Boolean(string = "Would you like to have your solution to receive updates?", required = True)

    users = fields.Integer(string = "Amount of users", required = True)
    time_deploy = fields.Selection([
        ('none', 'None'),
        ('some', 'Some'),
        ('unlimited', 'Unlimited')
    ], string = "Time from my personnel available to invest in deployment", default = "none", required = True)

    time_training = fields.Selection([
        ('none', 'None'),
        ('some', 'Some'),
        ('unlimited', 'Unlimited')
    ], string = "Time available from my personnel to invest in training", default = "none", required = True)

    budget_option = fields.Selection([
        ('composed', 'Upfront + Yearly'),
        ('total', 'Total Budget')
    ], string = "Budget format", default = "composed")

    critical = fields.Boolean(string = "Is this solution critical? (i.e. if the solution fails operation stops)")

    order_by = fields.Selection([
        ('overall', 'Overall Evaluation'),
        ('technical', 'Technical Evaluation'),
        ('characteristic', 'Characteristic Evaluation'),
        ('feedback', 'Feedback Evaluation')
    ], string = "Order By", default = "overall")

    status = fields.Selection([
        ('draft', 'Draft'),
        ('closed', 'Closed'),
        ('implemented', 'Implemented')
    ], string = "Status", default = "draft")


    # Preload
    experience = fields.Boolean(string = "Do you have any previous experience with digital solution deployment?", required = True)
    team_digital = fields.Boolean(string = "Do you have a designated team for digital implementation?")
    technological_saavy = fields.Selection([
        ('highest','Highly Saavy (Developers, Configurators)'),
        ('high', 'Saavy (Native Digital Users)'),
        ('medium', 'OK (Proficient Computer User)'),
        ('low','Low (User with difficulties)'),
        ('lowest','Lacking (No CPU use at all)')
    ], string = "Indicate how technological saavy is your team in average", default = "medium",required = True)
    coding = fields.Boolean(string = "Do you have anyone with coding skills?")

    @api.model
    def create(self, vals):
        num_search= self.env['shoe.searches'].search([('name', '!=', '')])
        if num_search:
            num = len(num_search) +1
        else:
            num = 1
        num = "{:04d}".format(num)
        new_search = super(search, self).create(vals)
        new_search.code = str(num)
        current_datetime = datetime.datetime.now()
        new_search.date = current_datetime.date()
        
        time_string = current_datetime.time().strftime('%H:%M:%S')
        
        new_search.time = time_string
        user = self.env.user.id
        sme = self.env['shoe.smes'].search([('user', '=', user)])
        new_search.team_digital = sme.team_digital
        new_search.experience = sme.experience
        new_search.technological_saavy = sme.technological_saavy
        new_search.coding = sme.coding

        list_skills = []

        for element in sme.skills:
            list_skills.append(element.id)

        new_search.skills = [(6,0, list_skills)]

        if sme:
            new_search.sme = sme.id

        return new_search

    def add_function(self):

        if self.functionalities:
            for element in self.functionalities:
                match = self.env['shoe.weighted.functionalities'].search([('functionalities', '=', element.id), ('searching', '=', self.id)])
                if match:
                    raise ValidationError("Functionalities already in the wishlist")
                else:
                    dict_create = {'name': element.name,
                        'functionalities': element.id,
                        'weight' : 1,
                        'searching' : self.id,
                    }
                    weighted = self.env["shoe.weighted.functionalities"].create(dict_create)
                    self.weighted_functionalities = [(4,weighted._origin.id)]
            self.functionalities = [(5,)]
        else:
            raise ValidationError("Insert functionalities in the field")

    def evaluate_solutions(self):

        if self.budget_option == "composed":
            yearly_budget = self.yearly_budget_max
            upfront_budget = self.upfront_budget_max
        else:
            upfront_budget = self.total_budget_max
            yearly_budget = 0


        if yearly_budget > 0:
            if self.critical:
                if self.users >= 10:
                    recommended_cost_scheme = 'subscription'
                else:
                    recommended_cost_scheme = 'usage'
            else:
                if self.tailored == 'generic':
                    recommended_cost_scheme = 'fremium'
                else:
                    if self.users >= 10:
                        recommended_cost_scheme = 'subscription'
                    else:
                        recommended_cost_scheme = 'usage'
        else:
            recommended_cost_scheme = 'one'


        user_friendliness_level = 0
        training_level = 0
        testing_level = 4

        if self.technological_saavy == 'highest':
            pass
        elif self.technological_saavy == 'high':
            user_friendliness_level += 1
            training_level += 1
        elif self.technological_saavy == 'medium':
            user_friendliness_level += 2
            training_level += 2
        elif self.technological_saavy == 'low':
            user_friendliness_level += 3
            training_level += 3
        else:
            user_friendliness_level += 4
            training_level += 4
        
        if not self.coding:
            user_friendliness_level += 1
        
        if not self.team_digital:
            user_friendliness_level += 1
            training_level += 3
            testing_level += 3
        
        if not self.experience:
            user_friendliness_level += 1
            training_level += 3
        
        if self.time_training == 'none':
            user_friendliness_level += 3
        elif self.time_training == 'some':
            user_friendliness_level += 2
        else:
            user_friendliness_level += 1

        if self.time_deploy != 'none':
            testing_level += 3

        if user_friendliness_level == 0 and self.time_deploy == 'unlimited' and self.tailored == 'generic':
            recommended_deployment = 'solo'
        else:
            if (self.technological_saavy == 'high' or self.technological_saavy == 'highest') and self.experience and self.time_deploy != 'none':
                recommended_deployment = 'assisted'
            else:
                recommended_deployment = 'full'

        if self.tailored == 'none':
            config_level = 'fixed'
            custom_level = 'fixed'
        elif self.tailored == 'some':
            if (self.technological_saavy == 'high' or self.technological_saavy == 'highest'):
                config_level = 'ample'
                custom_level = 'limited'
            else:
                config_level = 'limited'
                custom_level = 'ample'
        else:
            if (self.technological_saavy == 'high' or self.technological_saavy == 'highest') and self.time_deploy == 'unlimited':
                config_level = 'full'
                custom_level = 'ample'
            else:
                custom_level = 'full'
                config_level = 'ample'

        if user_friendliness_level == 0 and not self.critical:
            support_level = 'none'
        else:
            if self.critical:
                support_level = 'all'
            else:
                support_level = 'working'

        list_skills = []
        for element in self.skills:
            list_skills.append(element.id)

        list_weighted_functionalities= []
        for element in self.weighted_functionalities:
            list_weighted_functionalities.append(element.id)

        return {
            "name": "Search Wizard",
            'type': 'ir.actions.act_window',
            'res_model': 'shoe.search.wizard',
            'target': 'new',
            'views': [[False, 'form']],
            "context": {'default_name': self.name,
                        'default_searching': self.id,
                        'default_upfront_budget_max': upfront_budget,
                        'default_yearly_budget_max': yearly_budget,
                        'default_user_friendliness_level': user_friendliness_level,
                        'default_training_level': training_level,
                        'default_testing_level' : testing_level,
                        'default_skills': list_skills,
                        'default_cost_scheme': recommended_cost_scheme,
                        'default_customization_level': custom_level,
                        'default_configurability_level': config_level,
                        'default_support_availability': support_level,
                        'default_weighted_functionalities': list_weighted_functionalities,
                        'default_deployment': recommended_deployment},
            "view_id": "shoe_search_wizard"
        }

    def select_solution(self):
        solutions = []
        for element in self.solutions:
            solutions.append(element.solution.id)
        pass


    def close_query(self):
        self.status = 'closed'


class ratings(models.Model):
    _name = "shoe.ratings"
    name = fields.Char(string = "Title")
    comment = fields.Text(string = "Comment")

class suppliers(models.Model):
    _name = 'shoe.suppliers'

    name = fields.Char(string= "Supplier")
    code = fields.Char(string = "Code")
    solutions = fields.Many2many('shoe.technologies', string = "Solutions")

    # Location
    country = fields.Many2one('res.country',string = "Country")
    state = fields.Many2one('res.country.state', string="State", store=True)
    city = fields.Char(string = "City")

    @api.onchange('country')
    def set_values_to(self):
        if self.country:
            ids = self.env['res.country.state'].search([('country_id', '=', self.country.id)])
            return {
                'domain': {'state': [('id', 'in', ids.ids)],}
            }

    def action_view_comments(self):
        pass
    
    def action_view_implementations(self):
        pass

    # Company's Contact Information
    website = fields.Char(string ="Web Site", required = True)
    phone_number = fields.Char(string = "Company's Number", required = True)

    # Contact Information
    contact = fields.Char(string = "Name of Contact", required = True)
    phone_number_contact = fields.Char(string = "Contact's Number")
    email_contact = fields.Char(string = "Email")

    # Stats
    comments = fields.Integer(string = "Feedbacks")
    implementations = fields.Integer(string = "Implementations")

    # User
    user = fields.Many2one('res.user', string = "User")

    @api.model
    def create(self, vals):
        sup= self.env['shoe.suppliers'].search([('name', '!=', '')])
        if sup:
            num = len(sup) +1
        else:
            num = 1
        num = "{:04d}".format(num)
        supplier = super(suppliers, self).create(vals)
        supplier.code = str(num)
        return supplier