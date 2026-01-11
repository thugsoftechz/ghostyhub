#ifndef _GHOST_SCHED_H
#define _GHOST_SCHED_H

#include <linux/sched.h>

/* Ghost Scheduler Definitions */
#define SCHED_GHOST_GAME 7

bool ghost_is_game(struct task_struct *p);

#endif /* _GHOST_SCHED_H */
