import time
import uuid

make_uuid = lambda : str(uuid.uuid4())
make_time = lambda : time.strftime("%Y-%m-%d %H:%M:%S")

class StepperMotor(object):

    name = None
    initialized = False
    delay = 0.0001
    control_pins = [7, 9, 11, 13]
    position = 0
    min_position = 0
    max_position = 10
    sequence = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

    def __init__(self, name=None):
        self.name = name
        # setup pins
        for pin in self.control_pins:
            self.gpio("setup", pin, False)
        self.initialized = True

    def __repr__(self):
        return "<StepperMotor name={} position={}>".format(repr(self.name), self.position)

    def gpio(self, cmd, *args):
        print(f"GPIO.{cmd}{args}")
        # fn = GPIO.getattr(cmd, lambda *x : ValueError(f"Invalid GPIO command: {cmd}"))
        # fn(*args)
        return True

    def zero(self):
        print(f"zeroing position")
        # should we set as min_position or as midpoint?
        self.position = 0
        return self.position

    def increment(self):
        print(f"incrementing 1 step...")
        for seq in self.sequence:
            for pin, power in zip(self.control_pins, seq):
                self.gpio("set_output", pin, power)
            time.sleep(self.delay)
        self.position += 1
        return self.position

    def decrement(self):
        print(f"decrementing 1 step...")
        for seq in self.sequence[::]:
            for pin, power in zip(self.control_pins, seq):
                self.gpio("set_output", pin, power)
            time.sleep(self.delay)
        self.position -= 1
        return self.position

    def visit(self, position):
        # bounds check
        if (position < self.min_position) or (position > self.max_position):
            if position < self.min_position:
                position = self.min_position
            elif position > self.max_position:
                position = self.max_position
            print(f"cannot travel outside of bounds, limiting to: {position}")
        # evaluate using while-loop vs. explicit step counting
        distance = position - self.position
        operation = [self.increment, self.decrement][self.position > position]
        print(f"step distance: {distance} ({operation.__qualname__})")
        for _ in range(abs(distance)):
            operation()
        print(f"reached destination for stepper: {self.name}")
        return True

# ---
class Manager(object):
    # StepperMotorManager
    # PresetManager (presets, groups, favorites)
    # ConfigurationManager

    # split json files into preset/groups/motors
    """
    preset = {
        "id": uuid,
        "name": str,
        "description": str,
        "group": uuid (group.id),
        "position": {
            "X": 0,
            "Y": 0
        }
    }

    group = {
        "id": uuid,
        "name": str,
        "description": str
    }
    """
    config = {}
    steppers = {}
    presets = {}
    groups = {}
    
    active_preset = None

    def __init__(self, steppers=[]):
        # load global config from json file
        # load steppers from json file
        self.steppers = { s.name: s for s in steppers }
        # load presets from json file

    def __repr__(self):
        return "<Manager steppers={}>".format(self.position)

    @property
    def position(self):
        return { k: v.position for k,v in self.steppers.items() }

    def visit(self, **positions):
        for key, val in positions.items():
            self.steppers[key].visit(val)
        return True

    def create_preset(self, name=None, description=None, group=None, favorite=False):
        id = make_uuid()
        preset = {
            id: dict(
                id=id,
                name=name if name else make_time(),
                description=description,
                position=self.position,
                favorite=favorite,
                group=group
            )
        }
        print(f"creating new preset: {preset}")
        self.presets.update(preset)
        return id

    def load_preset(self, id):
        print(f"loading preset: {id}")
        preset = self.presets.get(id)
        if not preset:
            raise KeyError(f"No such preset with id: {id}")
        self.visit(**preset["position"])
        self.active_preset = id
        return id
    
    def create_group(self, name=None, description=None):
        id = make_uuid()
        group = {
            id: dict(
                id=id,
                name=name if name else make_time(),
                description=description
            )
        }
        print(f"creating new group: {group}")
        self.groups.update(group)
        return id

    


if __name__ == "__main__":
    # stepper = StepperMotor("X")
    # print(stepper)
    # print(stepper.position)
    # stepper.visit(5)
    # print(stepper.position)
    # stepper.visit(-5)
    # print(stepper.position)

    manager = Manager(steppers=[
        StepperMotor(name="X"),
        StepperMotor(name="Y")
    ])
    print(manager)
    print(manager.position)
    manager.visit(X=1, Y=3)
    print(manager.position)
    
    preset_id = manager.create_preset()
    manager.visit(X=3, Y=1)
    # manager.update_preset("77d10bd8-674f-4ef7-b24a-d59281d69ec5")
    # manager.delete_preset("77d10bd8-674f-4ef7-b24a-d59281d69ec5")
    manager.load_preset(preset_id)
    print(manager.position)
    # group_id = manager.create_group()
    # manager.update_group("77d10bd8-674f-4ef7-b24a-d59281d69ec5")
    # manager.delete_group("77d10bd8-674f-4ef7-b24a-d59281d69ec5")
    
    print(manager.steppers["X"].increment()) # + button
    print(manager.steppers["X"].decrement()) # - button
    
    print(manager.steppers["Y"].increment()) # + button
    print(manager.steppers["Y"].decrement()) # - button
    
    # button pressed -> operation performed -> position updated -> operation completes -> display new position
