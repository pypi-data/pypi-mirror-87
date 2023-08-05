# Copyright 2015 Hewlett-Packard Development Company, L.P.
# Copyright 2019 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# Hewlett Packard Enterprise made changes in this file.

import mock
from sdflexutils import exception
from sdflexutils.hpssa import disk_allocator
from sdflexutils.hpssa import objects
from sdflexutils.tests.unit.hpssa import raid_constants
import testtools


@mock.patch.object(objects.Server, '_get_all_details')
class DiskAllocatorTestCase(testtools.TestCase):

    def test__get_criteria_matching_disks_all_criterias(self,
                                                        get_all_details_mock):
        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        server = objects.Server()
        physical_drives = server.controllers[0].unassigned_physical_drives

        logical_disk = {'size_gb': 100,
                        'raid_level': '1',
                        'disk_type': 'ssd',
                        'interface_type': 'sata',
                        'model': 'ATA     MK000500GWEZH',
                        'firmware': 'HPGB'}

        ret_physical_drives = disk_allocator._get_criteria_matching_disks(
            logical_disk, physical_drives)
        self.assertEqual(ret_physical_drives, physical_drives)

    def test__get_criteria_matching_disks_not_all_criterias(
            self, get_all_details_mock):
        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        server = objects.Server()
        physical_drives = server.controllers[0].unassigned_physical_drives

        logical_disk = {'size_gb': 100,
                        'raid_level': '1',
                        'disk_type': 'ssd',
                        'interface_type': 'sata',
                        'firmware': 'HPGB'}

        ret_physical_drives = disk_allocator._get_criteria_matching_disks(
            logical_disk, physical_drives)
        self.assertEqual(ret_physical_drives, physical_drives)

    def test__get_criteria_matching_disks_some_disks_dont_match(
            self, get_all_details_mock):
        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        server = objects.Server()
        physical_drives = server.controllers[0].unassigned_physical_drives

        logical_disk = {'size_gb': 100,
                        'raid_level': '1',
                        'disk_type': 'ssd',
                        'interface_type': 'sata',
                        'firmware': 'HPGB'}

        physical_drives[0].disk_type = 'hdd'
        physical_drives[1].firmware = 'asdf'
        ret_physical_drives = disk_allocator._get_criteria_matching_disks(
            logical_disk, physical_drives)
        exp_physical_drives = physical_drives[2:]
        self.assertEqual(exp_physical_drives, ret_physical_drives)

    def test__get_criteria_matching_disks_no_disks_match(
            self, get_all_details_mock):
        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        server = objects.Server()
        physical_drives = server.controllers[0].unassigned_physical_drives

        logical_disk = {'size_gb': 100,
                        'raid_level': '1',
                        'disk_type': 'ssdd',
                        'interface_type': 'sas',
                        'firmware': 'HPD6'}

        ret_physical_drives = disk_allocator._get_criteria_matching_disks(
            logical_disk, physical_drives)
        self.assertFalse(ret_physical_drives)

    def test_allocate_disks_okay(self, get_all_details_mock):
        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        server = objects.Server()

        logical_disk = {'size_gb': 100,
                        'raid_level': '1',
                        'disk_type': 'ssd',
                        'interface_type': 'sata'}

        # Decrease size of two disks so that they get selected.
        disk1 = server.controllers[0].get_physical_drive_by_id('CN1:1:3')
        disk2 = server.controllers[0].get_physical_drive_by_id('CN1:1:12')
        disk1.size_gb = 100
        disk2.size_gb = 100

        raid_config = {'logical_disks': [logical_disk]}
        disk_allocator.allocate_disks(logical_disk, server, raid_config)
        self.assertEqual('MSCC SmartRAID 3154-8e in Slot 2085',
                         logical_disk['controller'])
        self.assertEqual(sorted(['CN1:1:3', 'CN1:1:12']),
                         sorted(logical_disk['physical_disks']))

    def test_allocate_disks_max_okay(self, get_all_details_mock):
        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        server = objects.Server()

        logical_disk = {'size_gb': 'MAX',
                        'raid_level': '1',
                        'disk_type': 'ssd',
                        'interface_type': 'sata'}

        # Decrease size of three disks so that the remaining gets
        # selected.
        disk1 = server.controllers[0].get_physical_drive_by_id('CN1:1:3')
        disk2 = server.controllers[0].get_physical_drive_by_id('CN1:1:12')
        disk3 = server.controllers[0].get_physical_drive_by_id('CN1:1:4')
        disk1.size_gb = 300
        disk2.size_gb = 300
        disk3.size_gb = 300

        raid_config = {'logical_disks': [logical_disk]}
        disk_allocator.allocate_disks(logical_disk, server, raid_config)
        self.assertEqual('MSCC SmartRAID 3154-8e in Slot 2085',
                         logical_disk['controller'])
        self.assertEqual(sorted(['CN1:1:5', 'CN1:1:11']),
                         sorted(logical_disk['physical_disks']))

    def test_allocate_disks_disk_size_not_matching(self,
                                                   get_all_details_mock):
        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        server = objects.Server()

        logical_disk = {'size_gb': 700,
                        'raid_level': '1',
                        'disk_type': 'hdd',
                        'interface_type': 'sas'}
        raid_config = {'logical_disks': [logical_disk]}
        exc = self.assertRaises(exception.PhysicalDisksNotFoundError,
                                disk_allocator.allocate_disks,
                                logical_disk, server, raid_config)
        self.assertIn("of size 700 GB and raid level 1", str(exc))

    def test_allocate_disks_disk_not_enough_disks(self,
                                                  get_all_details_mock):
        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        server = objects.Server()
        physical_drives = server.controllers[0].unassigned_physical_drives
        physical_drives = physical_drives[:2]
        server.controllers[0].unassigned_physical_drives = physical_drives

        logical_disk = {'size_gb': 600,
                        'raid_level': '5',
                        'disk_type': 'hdd',
                        'interface_type': 'sas'}
        raid_config = {'logical_disks': [logical_disk]}
        exc = self.assertRaises(exception.PhysicalDisksNotFoundError,
                                disk_allocator.allocate_disks,
                                logical_disk, server, raid_config)
        self.assertIn("of size 600 GB and raid level 5", str(exc))

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_allocate_disks_share_physical_disks(self, execute_mock,
                                                 get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.ONE_DRIVE_RAID_1
        execute_mock.return_value = (
            raid_constants.DRIVE_2_RAID_1_OKAY_TO_SHARE, None)

        rdh = {'wwn': '0x600508b1001c02bd'}
        controller = 'MSCC SmartRAID 3154-8e in Slot 2085'
        physical_disks = ['CN1:1:1', 'CN1:1:2']

        raid_config = {'logical_disks': [{'size_gb': 50,
                                          'raid_level': '1',
                                          'share_physical_disks': True,
                                          'root_device_hint': rdh,
                                          'controller': controller,
                                          'physical_disks': physical_disks},
                                         {'size_gb': 50,
                                          'raid_level': '1',
                                          'share_physical_disks': True}]}

        logical_disk = raid_config['logical_disks'][1]
        server = objects.Server()
        disk_allocator.allocate_disks(logical_disk, server, raid_config)
        self.assertEqual(controller, logical_disk['controller'])
        self.assertEqual('A', logical_disk['array'])
        self.assertNotIn('physical_disks', logical_disk)

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_allocate_disks_share_physical_disks_no_space(
            self, execute_mock, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.ONE_DRIVE_RAID_1
        execute_mock.return_value = (
            raid_constants.DRIVE_2_RAID_1_OKAY_TO_SHARE, None)

        rdh = {'wwn': '0x600508b1001c02bd'}
        controller = 'MSCC SmartRAID 3154-8e in Slot 2085'
        physical_disks = ['CN1:1:1', 'CN1:1:2']

        raid_config = {'logical_disks': [{'size_gb': 50,
                                          'raid_level': '1',
                                          'share_physical_disks': True,
                                          'root_device_hint': rdh,
                                          'controller': controller,
                                          'physical_disks': physical_disks},
                                         {'size_gb': 600,
                                          'raid_level': '1',
                                          'share_physical_disks': True}]}

        logical_disk = raid_config['logical_disks'][1]
        server = objects.Server()
        self.assertRaises(exception.PhysicalDisksNotFoundError,
                          disk_allocator.allocate_disks,
                          logical_disk, server, raid_config)

    def test_allocate_disks_share_physical_disks_criteria_mismatch(
            self, get_all_details_mock):

        # Both the drives don't have firmware HPD6
        get_all_details_mock.return_value = raid_constants.ONE_DRIVE_RAID_1

        rdh = {'wwn': '0x600508b1001c02bd'}
        controller = 'MSCC SmartRAID 3154-8e in Slot 2085'
        physical_disks = ['CN1:1:1', 'CN1:1:2']

        raid_config = {'logical_disks': [{'size_gb': 50,
                                          'raid_level': '1',
                                          'share_physical_disks': True,
                                          'root_device_hint': rdh,
                                          'controller': controller,
                                          'physical_disks': physical_disks},
                                         {'size_gb': 50,
                                          'raid_level': '1',
                                          'firmware': 'HPD6',
                                          'share_physical_disks': True}]}

        logical_disk = raid_config['logical_disks'][1]
        server = objects.Server()
        self.assertRaises(exception.PhysicalDisksNotFoundError,
                          disk_allocator.allocate_disks,
                          logical_disk, server, raid_config)
