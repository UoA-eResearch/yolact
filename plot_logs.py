#!/usr/bin/env python3
from utils.logger import LogVisualizer
vis = LogVisualizer()

vis.sessions('logs/sidewalks.log')
vis.add('logs/sidewalks.log', session=[8,9])
vis.plot('train', 'x.data.epoch', 'x.data.loss.T', smoothness=100)
vis.plot('val', 'x.data.epoch', 'x.data.mask["all"]', smoothness=100)
vis.bar('val', 'x.data.mask', x_idx=-1)