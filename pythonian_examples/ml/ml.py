import logging
logger = logging.getLogger('MLAgent')

import numpy as np
import numpy.ma as ma

from numpy.linalg import lstsq



def learn(labels, feats, out):

	logger.debug(labels)

	labels_mat = np.array(labels)
	feats_mat = np.transpose(np.array(feats, dtype='float').squeeze())
	out_mat = np.array(out, dtype='float')

	# tidy up the data
	(labels_clean, feats_clean) = clean_data(labels_mat, feats_mat, out_mat)

	# logger.debug("clean stuff is " + np.array_str(labels_clean) + " " + np.array_str(feats_clean))

	sln = linreg(feats_clean, out_mat)

	# logger.debug(sln)

	return np.array_str(sln)


# clean up the data. maybe pre-filter based on some inforamtion-theoretic methods
# right now just simply remove uniform columns
def clean_data(labels, feats, out):
	# return a mask designating whether each column is uniform and negate it
	mask = ~np.all(feats == feats[0,:], axis=1)
	return (labels[mask], np.compress(mask, feats, axis=1))



def linreg(data, out):
	(x, res, rank, s) = lstsq(data, out, rcond=None)
	return x