# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from xml.dom import ValidationErr
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class search_wizard(models.TransientModel):
    _name = 'shoe.search.wizard'
    _description = 'Search Wizard'

    name = fields.Char(string = "Title")
    upfront_budget_max = fields.Float(string = "Upfront Budget", required = True)
    yearly_budget_max = fields.Float(string = "Yearly Budget", required = True)

    user_friendliness_level = fields.Integer(string = "User Friendliness Level (0-10)", required = True)
    training_level = fields.Integer(string = "Training Level (0-10)", required = True)
    testing_level = fields.Integer(string = "Testing Level (0-10)", required = True)

    searching = fields.Many2one('shoe.searches', string = "Searches")

    skills = fields.Many2many('shoe.skills', string = "Skills")

    cost_scheme = fields.Selection([
        ('freemium', 'Freemium'),
        ('subscription', 'Tiered Subscription'),
        ('usage', 'Usage-based'),
        ('one', 'One-time')
    ], string = "Cost Scheme", default = "subscription", required = True)

    deployment = fields.Selection([
        ('full', 'Full deployment'),
        ('assisted', 'Assisted'),
        ('solo', 'No assistance')
    ], string = "Type of deployment provided to the customer", default = "full", required = True)

    customization_level = fields.Selection([
        ('fixed','One solution no customization available'),
        ('limited', 'Limited customization (i.e. add fields or custom views)'),
        ('ample', 'Customization able to adapt to customer needs'),
        ('full', 'Full customized solution')
    ], string = "Customization Level", required = True)

    configurability_level = fields.Selection([
        ('fixed','Not able for user to configure the solution'),
        ('limited','User can modify specific parts of the solution'),
        ('ample','User can modify the majority of the solution'),
        ('full','User can completely configure the solution')
    ], string = "Configurability Level", required = True)

    support_availability = fields.Selection([
        ('all', '24/7'),
        ('working', 'Working hours'),
        ('none', 'None')
    ], string = "Support Availability (select closest)", required = True)

    weighted_functionalities = fields.Many2many('shoe.weighted.functionalities',string = "Wishlist", required = True)

    def searching_solutions(self):
        # for element in self.searching.solutions:
        #     self.searching.solutions = (3, element.id)
        option_list = []
        solutions_ids = []
        solutions_functional_eval = []
        for element in self.weighted_functionalities:
            match= self.env['shoe.technologies'].search([('functionalities', 'in', [element.functionalities.id])])
            for m in match:
                if m.id not in solutions_ids:
                    solutions_ids.append(m.id)
                    solutions_functional_eval.append(element.weight)
                else:
                    index = solutions_ids.index(m.id)
                    solutions_functional_eval[index] = solutions_functional_eval[index] + element.weight
        
        count = 0

        for element in solutions_ids:
            match = self.env['shoe.technologies'].search([('id', '=', element)])
            if match:
                solution = match[0]

                # Cost
                cost = 0

                if self.customization_level == 'fixed':
                    ratio =  solution.upfront_cost / self.upfront_budget_max
                else:
                    ratio =  (solution.upfront_cost + solution.customization_cost) / self.upfront_budget_max

                if ratio  > 2:
                    cost = 0
                elif ratio > 1:
                    cost += 2
                else:
                    cost += 5
                
                if self.support_availability == 'none':
                    ratio = solution.total_yearly_cost / self.yearly_budget_max
                else:
                    ratio = (solution.total_yearly_cost + solution.support_cost) / self.yearly_budget_max 
                if ratio  > 2:
                    cost = 0
                elif ratio > 1:
                    cost +=2
                else:
                    cost += 5
                
                # Cost Scheme
                scheme = solution.cost_scheme

                cost_scheme = 0

                if scheme == self.cost_scheme:
                    cost_scheme = 10
                else:
                    if (scheme == 'one' and self.cost_scheme != 'one') or (scheme != 'one' and self.cost_scheme == 'one'):
                        cost_scheme = 0
                    else:
                        cost_scheme = 5
                
                # User friendliness
                user_friendliness = 0

                solution_user_level = 0

                total_skills = 0
                nailed_skills = 0
                for skill in solution.skills_use:
                    total_skills += 1
                    if skill in self.skills:
                        nailed_skills += 1
                percentage_skills = nailed_skills / total_skills

                if solution.manuals:
                    solution_user_level += 2.5
                
                if solution.help != 'no':
                    solution_user_level += 2.5

                solution_user_level = solution_user_level + 5 * percentage_skills

                if solution_user_level >= self.user_friendliness_level:
                    user_friendliness = 10
                else:
                    user_friendliness = 10 * (solution_user_level / self.user_friendliness_level)
                
                # Testing
                testing = 0
                solution_testing_level = 0

                if solution.test:
                    solution_testing_level += 2
                
                if solution.test_free:
                    solution_testing_level += 2
                
                if solution.test_limit or solution.lenght_trail > 30:
                    solution_testing_level += 2
                elif solution.lenght_trail > 15:
                    solution_testing_level += 1
                
                if solution.deepness_trail > 80:
                    solution_testing_level += 2
                elif solution.deepness_trail > 50:
                    solution_testing_level += 1
                
                if not (solution.cost_trail > 0):
                    solution_testing_level += 2

                if solution_testing_level >= self.testing_level:
                    testing = 10
                else:
                    testing = 10*(solution_testing_level / self.testing_level)

                # Training
                training = 0
                solution_training_level = 0

                if solution.training_free:
                    if solution.hours_free >= 100:
                        solution_training_level = 10
                    elif solution.hours_free >= 40:
                        solution_training_level = 7
                        if solution.training_cost:
                            rate = solution.cost_training / solution.hours_cost
                            if 100 > rate:
                                solution_training_level = 8
                    else:
                        solution_training_level = 4
                        if solution.training_cost:
                            rate = solution.cost_training / solution.hours_cost
                            if 100 > rate:
                                solution_training_level = 5
                else:
                    solution_training_level = 0
                    if solution.training_cost:
                        rate = solution.cost_training / solution.hours_cost
                        if 100 > rate:
                            solution_training_level = 1
                
                if solution_training_level >= self.training_level:
                    training = 10
                else:
                    training = 10*(solution_training_level / self.training_level)
                
                # Deployment
                deploy = solution.deployment

                deployment = 0

                if deploy == 'full':
                    solution_deployment_level = 2
                elif deploy == 'assisted':
                    solution_deployment_level = 1
                else:
                    solution_deployment_level = 0

                if self.deployment == 'full':
                    wish_deployment = 2
                elif self.deployment == 'assisted':
                    wish_deployment = 1
                else:
                    wish_deployment = 0

                if solution_deployment_level >= wish_deployment:
                    deployment = 10
                else:
                    if solution_deployment_level > 0 and wish_deployment > 0:
                        deployment = 7
                    elif wish_deployment == 1:
                        deployment = 3
                    else: 
                        deployment = 0

                # Customization
                customization = 0
                custom = solution.customization_level

                if custom == 'full':
                    solution_custom_level = 3
                elif custom == 'ample':
                    solution_custom_level = 2
                elif custom == 'limited':
                    solution_custom_level = 2
                else:
                    solution_custom_level = 0

                if self.customization_level == 'full':
                    wish_custom = 3
                elif self.customization_level == 'ample':
                    wish_custom = 2
                elif self.customization_level == 'limited':
                    wish_custom = 1
                else:
                    wish_custom = 0

                if solution_custom_level >= wish_custom:
                    customization = 10
                else:
                    difference = wish_custom - solution_custom_level
                    if difference == 1:
                        customization = 7
                    elif difference == 2:
                        customization = 3
                    else: 
                        customization = 0     

                # Configurability
                configurability = 0
                config = solution.configurability_level

                if custom == 'full':
                    solution_config_level = 3
                elif custom == 'ample':
                    solution_config_level = 2
                elif custom == 'limited':
                    solution_config_level = 2
                else:
                    solution_config_level = 0

                if self.configurability_level == 'full':
                    wish_config = 3
                elif self.configurability_level == 'ample':
                    wish_config = 2
                elif self.configurability_level == 'limited':
                    wish_config = 1
                else:
                    wish_config = 0

                if solution_config_level >= wish_config:
                    configurability = 10
                else:
                    difference = wish_config - solution_config_level
                    if difference == 1:
                        configurability = 7
                    elif difference == 2:
                        configurability = 3
                    else: 
                        configurability = 0   

                total_skills = 0
                nailed_skills = 0
                for skill in solution.skills_configure:
                    total_skills += 1
                    if skill in self.skills:
                        nailed_skills += 1
                percentage_skills = nailed_skills / total_skills
                configurability = configurability * percentage_skills

                # Support
                support = 0

                if solution.support_presence:
                    if (self.support_availability == solution.support_availability) or (self.support_availability == 'working' and solution.support_availability == 'all'):
                        if solution.support_free:
                            support = 10
                        else:
                            support = 7
                    else:
                        if solution.support_free:
                            support = 5
                        else:
                            support = 3          
                else:
                    if self.support_availability == 'none':
                        support = 10
                    else:
                        support = 0
                
                characteristics_eval = (cost + cost_scheme + user_friendliness + training + testing + deployment + customization + configurability + support) /9
                feedback = solution.rating_stars
                dict_create = {'name': solution.name,
                    'solution': solution.id,
                    'eval_functionality': solutions_functional_eval[count],
                    'eval_characteristics': characteristics_eval,
                    'eval_cost': cost,
                    'eval_cost_scheme': cost_scheme,
                    'eval_user_friend': user_friendliness,
                    'eval_testing': testing,
                    'eval_training': training,
                    'eval_deployment': deployment,
                    'eval_customization': customization,
                    'eval_configurability': configurability,
                    'eval_support': support,
                    'eval_feedback': feedback,
                }
                option = self.env["shoe.technologies.options"].create(dict_create)
                
                option_list.append(option.id)
                
                #self.searching.solutions = [(4,option._origin.id)]
            count = count +1 
        if option_list:
            self.searching.solutions = [(6,0,option_list)]
        return