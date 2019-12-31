# -*- coding: utf-8 -*-

from odoo.tests import TransactionCase
from odoo.tests.common import Form
from odoo.exceptions import AccessError

class TestModelCourse(TransactionCase):

    def setUp(self):
        super(TestModelCourse, self).setUp()
        self.group_manager = self.env.ref('openacademy.group_manager')
        self.test_user = self.env['res.users'].create({
            'name': 'John Doe',
            'login': 'test_user',
            'groups_id': [(4, self.group_manager.id)]
        })
        self.test_course = self.env['openacademy.course'].with_user(self.test_user).create({'name': 'Test course'})


    def test_create_course(self):
        self.assertTrue(self.test_course)
        self.assertEqual(self.test_course.name, 'Test course')


    def test_missing_name(self):
        f = Form(self.env['openacademy.course'])
        self.assertRaises(AssertionError, f.save)

    
    def test_only_manager_group_can_create(self):
        self.group_manager.write({'users': [(3, self.test_user.id)]})
        record = self.env['openacademy.course'].with_user(self.test_user)
        self.assertRaises(AccessError, record.create, [{'name': 'test'}])

    
    def test_only_manager_group_can_edit(self):
        self.group_manager.write({'users': [(3, self.test_user.id)]})
        self.assertRaises(AccessError, self.test_course.write, {'name': "new name"})


    def test_only_manager_group_can_delete(self):
        self.group_manager.write({'users': [(3, self.test_user.id)]})
        self.assertRaises(AccessError, self.test_course.unlink)


    def test_only_responsible_can_edit(self):
        self.test_course.write({'responsible_id': self.test_user})
        new_user = self.env['res.users'].create({
            'login': 'new_user',
            'name': 'New User'
        })
        record = self.test_course.with_user(new_user)
        self.assertRaises(AccessError, record.write, {'name': "new name"})


