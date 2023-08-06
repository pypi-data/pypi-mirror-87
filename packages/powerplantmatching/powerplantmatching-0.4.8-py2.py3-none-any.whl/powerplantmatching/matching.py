# -*- coding: utf-8 -*-
# Copyright 2016-2018 Fabian Hofmann (FIAS), Jonas Hoersch (KIT, IAI) and
# Fabian Gotzens (FZJ, IEK-STE)

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Functions for linking and combining different datasets
"""

from __future__ import absolute_import, print_function

from .core import get_config, _data_out, get_obj_if_Acc
from .utils import read_csv_if_string, parmap, get_name
from .duke import duke
from .cleaning import clean_technology

import os.path
import pandas as pd
import numpy as np
from itertools import combinations
import logging
logger = logging.getLogger(__name__)


def best_matches(links):
    """
    Subsequent to duke() with singlematch=True. Returns reduced list of
    matches on the base of the highest score for each duplicated entry.

    Parameters
    ----------
    links : pd.DataFrame
        Links as returned by duke
    """
    labels = links.columns.difference({'scores'})
    return (links
            .groupby(links.iloc[:, 1], as_index=False, sort=False)
            .apply(lambda x: x.loc[x.scores.idxmax(), labels]))


def compare_two_datasets(dfs, labels, use_saved_matches=False,
                         country_wise=True, config=None, **dukeargs):
    """
    Duke-based horizontal match of two databases. Returns the matched
    dataframe including only the matched entries in a multi-indexed
    pandas.Dataframe. Compares all properties of the given columns
    ['Name','Fueltype', 'Technology', 'Country',
    'Capacity','lat', 'lon'] in order to determine the same
    powerplant in different two datasets. The match is in one-to-one
    mode, that is every entry of the initial databases has maximally
    one link in order to obtain unique entries in the resulting
    dataframe.  Attention: When aborting this command, the duke
    process will still continue in the background, wait until the
    process is finished before restarting.

    Parameters
    ----------
    dfs : list of pandas.Dataframe or strings
        dataframes or csv-files to use for the matching
    labels : list of strings
        Names of the databases for the resulting dataframe


    """
    if config is None:
        config = get_config()

    dfs = list(map(read_csv_if_string, dfs))
    if not ('singlematch' in dukeargs):
        dukeargs['singlematch'] = True
    saving_path = _data_out('matches/matches_{}_{}.csv'
                            .format(*np.sort(labels)), config=config)
    if use_saved_matches:
        if os.path.exists(saving_path):
            logger.info('Reading saved matches for dfs {} and {}'
                        .format(*labels))
            return pd.read_csv(saving_path, index_col=0)
        else:
            logger.warning("Non-existing saved matches for dataset '{}', '{}'"
                           " continuing by matching again".format(*labels))

    def country_link(dfs, country):
        # country_selector for both dataframes
        sel_country_b = [df['Country'] == country for df in dfs]
        # only append if country appears in both dataframse
        if all(sel.any() for sel in sel_country_b):
            return duke([df[sel] for df, sel in zip(dfs, sel_country_b)],
                        labels, **dukeargs)
        else:
            return pd.DataFrame()

    if country_wise:
        countries = config['target_countries']
        links = pd.concat([country_link(dfs, c) for c in countries])
    else:
        links = duke(dfs, labels=labels, **dukeargs)
    matches = best_matches(links)
    matches.to_csv(saving_path)
    return matches


def cross_matches(sets_of_pairs, labels=None):
    """
    Combines multiple sets of pairs and returns one consistent
    dataframe. Identifiers of two datasets can appear in one row even
    though they did not match directly but indirectly through a
    connecting identifier of another database.

    Parameters
    ----------
    sets_of_pairs : list
        list of pd.Dataframe's containing only the matches (without
        scores), obtained from the linkfile (duke() and
        best_matches())
    labels : list of strings
        list of names of the databases, used for specifying the order
        of the output

    """
    m_all = sets_of_pairs
    if labels is None:
        labels = np.unique([x.columns for x in m_all])
    matches = pd.DataFrame(columns=labels)
    for i in labels:
        base = [m.set_index(i) for m in m_all if i in m]
        match_base = pd.concat(base, axis=1).reset_index()
        matches = pd.concat([matches, match_base], sort=True)

    matches = matches.drop_duplicates().reset_index(drop=True)
    for i in labels:
        matches = pd.concat([
            matches.groupby(i, as_index=False, sort=False)
                   .apply(lambda x: x.loc[x.isnull().sum(axis=1).idxmin()]),
            matches[matches[i].isnull()]
        ]).reset_index(drop=True)
    return (matches
            .assign(length=matches.notna().sum(axis=1))
            .sort_values(by='length', ascending=False)
            .reset_index(drop=True)
            .drop('length', axis=1)
            .reindex(columns=labels))


def link_multiple_datasets(datasets, labels, use_saved_matches=False,
                           config=None, **dukeargs):
    """
    Duke-based horizontal match of multiple databases. Returns the
    matching indices of the datasets. Compares all properties of the
    given columns ['Name','Fueltype', 'Technology', 'Country',
    'Capacity','lat', 'lon'] in order to determine the same
    powerplant in different datasets. The match is in one-to-one mode,
    that is every entry of the initial databases has maximally one
    link to the other database.  This leads to unique entries in the
    resulting dataframe.

    Parameters
    ----------
    datasets : list of pandas.Dataframe or strings
        dataframes or csv-files to use for the matching
    labels : list of strings
        Names of the databases in alphabetical order and corresponding
        order to the datasets
    """
    if config is None:
        config = get_config()

    dfs = list(map(read_csv_if_string, datasets))
    labels = [get_name(df) for df in dfs]

    combs = list(combinations(range(len(labels)), 2))

    def comp_dfs(dfs_lbs):
        logger.info('Comparing {0} with {1}'.format(*dfs_lbs[2:]))
        return compare_two_datasets(dfs_lbs[:2], dfs_lbs[2:],
                                    use_saved_matches=use_saved_matches,
                                    config=config, **dukeargs)

    mapargs = [[dfs[c], dfs[d], labels[c], labels[d]] for c, d in combs]
    all_matches = parmap(comp_dfs, mapargs)

    return cross_matches(all_matches, labels=labels)


def combine_multiple_datasets(datasets, labels=None, use_saved_matches=False,
                              config=None, **dukeargs):
    """
    Duke-based horizontal match of multiple databases. Returns the
    matched dataframe including only the matched entries in a
    multi-indexed pandas.Dataframe. Compares all properties of the
    given columns ['Name','Fueltype', 'Technology', 'Country',
    'Capacity','lat', 'lon'] in order to determine the same
    powerplant in different datasets. The match is in one-to-one mode,
    that is every entry of the initial databases has maximally one
    link to the other database.  This leads to unique entries in the
    resulting dataframe.

    Parameters
    ----------
    datasets : list of pandas.Dataframe or strings
        dataframes or csv-files to use for the matching
    labels : list of strings
        Names of the databases in alphabetical order and corresponding
        order to the datasets
    """
    if config is None:
        config = get_config()

    def combined_dataframe(cross_matches, datasets, config):
        """
        Use this function to create a matched dataframe on base of the
        cross matches and a list of the databases. Always order the
        database alphabetically.

        Parameters
        ----------
        cross_matches : pandas.Dataframe of the matching indexes of
            the databases, created with
            powerplant_collection.cross_matches()
        datasets : list of pandas.Dataframes or csv-files in the same
            order as in cross_matches
        """
        datasets = list(map(read_csv_if_string, datasets))
        for i, data in enumerate(datasets):
            datasets[i] = (data
                           .reindex(cross_matches.iloc[:, i])
                           .reset_index(drop=True))
        return (pd.concat(datasets, axis=1,
                          keys=cross_matches.columns.tolist())
                .reorder_levels([1, 0], axis=1)
                .reindex(columns=config['target_columns'], level=0)
                .reset_index(drop=True))
    crossmatches = link_multiple_datasets(datasets, labels,
                                          use_saved_matches=use_saved_matches,
                                          config=config, **dukeargs)
    return (combined_dataframe(crossmatches, datasets, config)
            .reindex(columns=config['target_columns'], level=0))


def reduce_matched_dataframe(df, show_orig_names=False, config=None):
    """
    Reduce a matched dataframe to a unique set of columns. For each entry
    take the value of the most reliable data source included in that match.

    Parameters
    ----------
    df : pandas.Dataframe
        MultiIndex dataframe with the matched powerplants, as obtained from
        combined_dataframe() or match_multiple_datasets()
    """
    df = get_obj_if_Acc(df)

    if config is None:
        config = get_config()

    # define which databases are present and get their reliability_score
    sources = df.columns.levels[1]
    rel_scores = pd.Series({s: config[s]['reliability_score'] for s in sources})\
                   .sort_values(ascending=False)
    cols = config['target_columns']
    props_for_groups = {col: 'first'
                        for col in cols}
    props_for_groups.update({'YearCommisisoned': 'min',
                             'DateRetrofit': 'max',
                             'projectID': lambda x: dict(x.droplevel(0).dropna()),
                             'eic_code': 'unique'})
    props_for_groups = pd.Series(props_for_groups)[cols].to_dict()

    # set low priority on Fueltype 'Other'
    # turn it since aggregating only possible for axis=0
    sdf = df.replace({'Fueltype': {'Other': np.nan}})\
            .stack(1).reindex(rel_scores.index, level=1)\
            .groupby(level=0)\
            .agg(props_for_groups)\
            .replace({'Fueltype': {np.nan: 'Other'}})

    if show_orig_names:
        sdf = sdf.assign(**dict(df.Name))
    return sdf.pipe(clean_technology).reset_index(drop=True)
