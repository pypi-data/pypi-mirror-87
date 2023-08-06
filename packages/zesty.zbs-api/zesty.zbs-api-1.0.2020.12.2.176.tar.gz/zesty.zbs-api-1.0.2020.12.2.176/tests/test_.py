import json

import pytest
from zesty.actions import *
from zesty.protocol import Metrics
ExtendFileSystemActionType = 'ExtendFileSystemAction'
BalanceEBSStructureActionType = 'BalanceEBSStructureAction'
BalanceFileSystemActionType = 'BalanceFileSystemAction'
RemoveDiskActionType = 'RemoveDiskAction'
AddDiskActionType = 'AddDiskAction'
DoNothingActionType = 'DoNothingAction'

TEST_MOUNT_PATH = "/dev/sda1"
TEST_DEVICE = "some_device"
TEST_FILE_SYSTEM = "ntfs"


def test_actions_factory():
    action: ExtendFileSystemAction = ZBSActionFactory.create_action(ExtendFileSystemActionType)
    assert action.get_action_type() == ExtendFileSystemActionType

    action1: ExtendFileSystemAction = ZBSActionFactory.create_action(ExtendFileSystemActionType)
    assert action1.get_action_type() == ExtendFileSystemActionType

    action2: BalanceEBSStructureAction = ZBSActionFactory.create_action(BalanceEBSStructureActionType)
    assert action2.get_action_type() == BalanceEBSStructureActionType

    action3: BalanceFileSystemAction = ZBSActionFactory.create_action(BalanceFileSystemActionType)
    assert action3.get_action_type() == BalanceFileSystemActionType

    action4: RemoveDiskAction = ZBSActionFactory.create_action(RemoveDiskActionType)
    assert action4.get_action_type() == RemoveDiskActionType

    action5: AddDiskAction = ZBSActionFactory.create_action(AddDiskActionType)
    assert action5.get_action_type() == AddDiskActionType

    action6: DoNothingAction = ZBSActionFactory.create_action(DoNothingActionType)
    assert action6.get_action_type() == DoNothingActionType


def test_action_serialization_and_deserialization():
    action: ExtendFileSystemAction = ZBSActionFactory.create_action(ExtendFileSystemActionType)
    action_data = ZBSActionData(TEST_MOUNT_PATH, TEST_DEVICE, TEST_FILE_SYSTEM)
    action.set_data(action_data)

    serialized_action = action.serialize()
    print("Action JSON is '{}'".format(serialized_action))

    deserialized_action_type = ZBSAction.deserialize_type(serialized_action)
    print("Deserialized action type is '{}'".format(deserialized_action_type))
    assert deserialized_action_type == ExtendFileSystemActionType

    deserialized_action_data = ZBSAction.deserialize_data(serialized_action)
    print("Deserialized Action data is '{}'".format(deserialized_action_data.mount_path))
    assert deserialized_action_data.mount_path == TEST_MOUNT_PATH
    assert deserialized_action_data.device == TEST_DEVICE
    assert deserialized_action_data.filesystem == TEST_FILE_SYSTEM

    received_action = ZBSActionFactory.create_action(deserialized_action_type)
    print("Got action of type '{}'".format(received_action.get_action_type()))
    assert received_action.get_action_type() == ExtendFileSystemActionType


class TestResponse(object):
    status_code = None
    raw_data = None

    def __init__(self, test_data):
        self.status_code = test_data.get('status_code')
        self.raw_data = test_data.get('raw_data')

    def json(self):
        return json.loads(json.dumps(self.raw_data))


def test_sending_over_network():
    action: ExtendFileSystemAction = ZBSActionFactory.create_action(ExtendFileSystemActionType)
    action_data = ZBSActionData(TEST_MOUNT_PATH, TEST_DEVICE, TEST_FILE_SYSTEM)
    action.set_data(action_data)

    serialized_action = action.serialize()

    response: Metrics.Response = Metrics.Response(TestResponse({"status_code": 202, "raw_data": serialized_action}))

    deserialized_action_type = ZBSAction.deserialize_type(serialized_action)
    assert deserialized_action_type == ExtendFileSystemActionType
