# -*- coding: utf-8 -*-

"""
@author: Quoc-Tuan Truong <tuantq.vnu@gmail.com>
"""

from collections import OrderedDict


class TestSet:
    """Test Set

    Parameters
    ----------
    user_ratings: :obj:`defaultdict` of :obj:`list`
        The dictionary containing lists of tuples of the form (item, rating). The keys are user ids.

    uid_map: :obj:`defaultdict`
        The dictionary containing mapping from original ids to mapped ids of users.

    iid_map: :obj:`defaultdict`
        The dictionary containing mapping from original ids to mapped ids of items.

    """

    def __init__(self, user_ratings, uid_map, iid_map):
        self._user_ratings = user_ratings
        self._uid_map = uid_map
        self._iid_map = iid_map

    def get_users(self):
        return self._user_ratings.keys()

    def get_ratings(self, mapped_uid):
        return self._user_ratings.get(mapped_uid, [])

    def get_uid(self, raw_uid):
        return self._uid_map[raw_uid]

    def get_iid(self, raw_iid):
        return self._iid_map[raw_iid]

    @classmethod
    def from_uir_triplets(self, triplet_data, global_uid_map, global_iid_map, global_ui_set, verbose=False):
        """Constructing TestSet from triplet data.

        Parameters
        ----------
        triplet_data: array-like, shape: [n_examples, 3]
            Data in the form of triplets (user, item, rating)

        global_uid_map: :obj:`defaultdict`
            The dictionary containing global mapping from original ids to mapped ids of users.

        global_iid_map: :obj:`defaultdict`
            The dictionary containing global mapping from original ids to mapped ids of items.

        global_ui_set: :obj:`set`
            The global set of tuples (user, item). This helps avoiding duplicate observations.

        verbose: bool, default: False
            The verbosity flag.

        Returns
        -------
        test_set: :obj:`<cornac.data.testset.TestSet>`
            Test set object.

        """

        uid_map = OrderedDict()
        iid_map = OrderedDict()
        user_ratings = {}

        unk_user_count = 0
        unk_item_count = 0

        for raw_uid, raw_iid, rating in triplet_data:
            if (raw_uid, raw_iid) in global_ui_set:  # duplicate rating
                continue
            global_ui_set.add((raw_uid, raw_iid))

            if not raw_uid in global_uid_map:
                unk_user_count += 1
            if not raw_iid in global_iid_map:
                unk_item_count += 1

            mapped_uid = global_uid_map.setdefault(raw_uid, len(global_uid_map))
            mapped_iid = global_iid_map.setdefault(raw_iid, len(global_iid_map))
            uid_map[raw_uid] = mapped_uid
            iid_map[raw_iid] = mapped_iid

            ur_list = user_ratings.setdefault(mapped_uid, [])
            ur_list.append((mapped_iid, float(rating)))

        if verbose:
            print('Number of tested users = {}'.format(len(user_ratings)))
            print('Number of unknown users = {}'.format(unk_user_count))
            print('Number of unknown items = {}'.format(unk_item_count))

        return self(user_ratings, uid_map, iid_map)
