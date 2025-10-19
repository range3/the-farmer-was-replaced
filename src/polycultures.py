import f0
import c
import parallel


def checker_black(x, y):
    return (x + y) % 2 == 0


def init(ofs_x, ofs_y, width, height):
    def iter():
        harvest()
        f0.till_to_grassland()
        if checker_black(get_pos_x(), get_pos_y()):
            plant(Entities.Tree)

    f0.move_to(ofs_x, ofs_y)
    f0.zigzag(width, height, iter)


def replant(ofs_x, ofs_y, width, height):
    def iter():
        f0.harvest_if_ready()
        if checker_black(get_pos_x(), get_pos_y()):
            plant(Entities.Tree)

    f0.move_to(ofs_x, ofs_y)
    f0.zigzag(width, height, iter)


def init_carrot(ofs_x, ofs_y, width, height):
    def iter():
        harvest()
        f0.till_to_soil()
        plant(Entities.Carrot)

    f0.move_to(ofs_x, ofs_y)
    f0.zigzag(width, height, iter)


def replant_carrot(ofs_x, ofs_y, width, height):
    def iter():
        f0.harvest_if_ready()
        plant(Entities.Carrot)

    f0.move_to(ofs_x, ofs_y)
    f0.zigzag(width, height, iter)


def naive(ofs_x, ofs_y, width, height, min_cycles, max_cycles, target_resources):
    companions = {}
    end_x = ofs_x + width
    end_y = ofs_y + height

    def zig(fn):
        f0.move_to(ofs_x, ofs_y)
        for y in range(ofs_y, end_y, 2):
            # --->
            for x in range(ofs_x, end_x - 1):
                fn(x, y)
                move(East)

            fn(x + 1, y)
            move(North)

            # <---
            for x in range(end_x - 1, ofs_x, -1):
                fn(x, y)
                move(West)

            fn(ofs_x, y)
            if y < end_y - 1:
                move(North)

    def _prepare(x, y):
        if get_ground_type() != Grounds.Soil:
            till()
        _naive(x, y)

    def _naive(x, y):
        harvest()
        while get_water() < 0.5:
            use_item(Items.Water)

        if (x, y) in companions:
            plant(companions.pop((x, y)))
        else:
            plant(Entities.Grass)

        companion, coords = get_companion()
        companions[coords] = companion

    def _should_continue(cycles):
        if cycles < min_cycles:
            return True

        if max_cycles and cycles >= max_cycles:
            return False

        if target_resources:
            for item in target_resources:
                target = target_resources[item]
                if target and num_items(item) >= target:
                    return False
        return True

    zig(_prepare)
    cycles = 1

    while _should_continue(cycles):
        zig(_naive)
        cycles += 1


def run(
    min_cycles=2,
    max_cycles=10,
    target_resources={
        Items.Hay: 1000**3,
        Items.Wood: 1000**3,
        Items.Carrot: 1000**3,
    },
):
    y_drones = c.WORLD_SIZE // 4
    x_drones = c.MAX_DRONES // y_drones
    width = c.WORLD_SIZE // x_drones
    height = 4

    for yd in range(y_drones - 1, -1, -1):
        for xd in range(x_drones - 1, -1, -1):
            ofs_x = width * xd
            ofs_y = height * yd

            def _fn():
                naive(
                    ofs_x,
                    ofs_y,
                    width,
                    height,
                    min_cycles,
                    max_cycles,
                    target_resources,
                )

            if not spawn_drone(_fn):
                _fn()
    
    parallel.wait_all()
