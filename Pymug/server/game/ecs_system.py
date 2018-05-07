#  functions to allow ECS Systems to run

import time


def ecs_clock_system_thread(db, q, messenger, system_name, system_func, component_name, component_predicates, update_seconds, tick_seconds):
    system_prop = 'pymug_ecs_system_{0}'.format(system_name)
    while True:
        start_time = time.time()
        matches = db.get_components_matching_predicates(component_name, component_predicates+[(system_prop, '<=', start_time-update_seconds, True)])
        for m in matches:
            messages = system_func(db, messenger, m)
            for m in messages:
                q.put(m)
            db.update_component_for_entity(component_name, {system_prop: time.time()}, m['entity'])
        elapsed = time.time()-start_time
        if elapsed < tick_seconds:
            time.sleep(tick_seconds-elapsed)

def ecs_timer_system_thread(db, q, messenger, system_name, system_func, update_seconds):
    last_run = 0
    while True:
        now = time.time()
        if now-last_run >= update_seconds:
            last_run = time.time()
            messages = system_func(db, messenger)
            for m in messages:
                q.put(m)
        now = time.time()
        if now-last_run < update_seconds:
            time.sleep(update_seconds - (now-last_run))