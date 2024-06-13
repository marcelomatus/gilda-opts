"""Contains the simulation module."""

from linear_problem import LinearProblem
from schedule import Schedule


class Simulation:
    """Scenery data container."""

    def create_schedule_lp(self, schedule: Schedule):
        """Create the scheduing LP."""
        lp = LinearProblem(scale_obj=schedule.options.scale_obj,
                           integer_mode=schedule.options.integer_mode)
        schedule_lp = ScheduleLPFactory().create(schedule)

        for st in self.stage.values():
            schedule_lp.add_stage_to_lp(st, lp)

        for sc in self.scenery.values():
            schedule_lp.add_scenery_to_lp(sc, lp)

        return schedule_lp, lp
