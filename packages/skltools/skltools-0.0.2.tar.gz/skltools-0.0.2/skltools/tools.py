import warnings
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted
import matplotlib.pyplot as plt
from typing import Any
import pandas as pd
import numpy as np
from sklearn.metrics import *
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection._split import _BaseKFold
from sklearn.utils.validation import *

warnings.filterwarnings('ignore')


class GroupTimeSeriesSplit(_BaseKFold):
	"""
	时序切分数据：增量滚动窗口切分，严格滚动窗口切分
	n_split: int, 默认为4, 即切分4次, 形成5块数据集

	Examples
	--------

	"""
	
	def __init__(self, n_splits=4):
		super().__init__(n_splits, shuffle=False, random_state=None)
	
	def split(self, X, y=None, groups=None, start_fold=3, forget=False):
		"""
		时序增量切分数据
		-----------------------------------------------
		:param X: pd.df or np.array
		:param y: pd.series or np.array
		:param groups: pd.Series or np.array;分组，同一组数据在同一数据集内；通常为时间
		:param start_fold: int, 默认为3；从第几个fold开始滚动；
			假设n_splits设置为4，数据被分为5块；
			start_fold为3，即第一个训练集为前3个fold，第一个测试集为第4个fold；
			之后按照1个fold向前滚动；第二个训练集为前4个fold，第二个测试集为第5个fold
		:param forget: bool；是否采用增量训练，即忘记过去的数据；True:严格滚动窗口，False:增量训练
		"""
		if (start_fold > self.n_splits) or (not isinstance(start_fold, int)):
			raise ValueError("[参数设置异常]-start_fold须为不超过n_splits的整数")
		if groups is None:
			raise ValueError("The 'groups' parameter should not be none")
		
		X, y, groups = indexable(X, y, groups)
		n_splits = self.n_splits
		n_folds = n_splits + 1
		
		# 取出组别的数量
		groups = check_array(groups, ensure_2d=False, dtype=None)
		unique_groups = np.unique(groups, return_inverse=True)[0]
		n_groups = len(unique_groups)
		
		# 如果组别不能整除，则去掉最前面的数据，去掉的样本数量等于余数
		if n_groups % n_folds != 0:
			print("[注意]-数据集组别除以数据集块（n_splits+1）的余数不为0\n"
			      "将去除时间最久的数据，以保证切分的每块数据集长度一致\n"
			      "如果groups不可剔除，则请重新设置n_splits")
			index_group = n_groups % n_folds
			unique_groups = unique_groups[index_group:]
			n_groups = len(unique_groups)
		
		# 计算每个fold中包含多少个group
		groups = np.array(groups)
		n_groups_per_fold = n_groups // n_folds
		
		# 采用增量训练，或是滚动窗口
		if forget:
			left_index = 'n_split'
		else:
			left_index = '0'
		
		for n_split in range(n_folds - start_fold):
			train_groups = unique_groups[eval(left_index):n_groups_per_fold * (
					n_split + start_fold)]
			test_groups = unique_groups[
			              n_groups_per_fold * (n_split + start_fold)
			              :n_groups_per_fold * (n_split + start_fold + 1)]
			yield (np.where(np.logical_and(groups >= train_groups[0],
			                               groups <= train_groups[-1]))[0],
			       np.where(np.logical_and(groups >= test_groups[0],
			                               groups <= test_groups[-1]))[0])


class RollingNanFiller(BaseEstimator, TransformerMixin):
	"""滚动填充nan值

	Parameters
	----------
	strategy: string, default='mean'
		填nan的策略.

		- If "mean", 用当前数据之前的均值填充目前的空值.
		- If "median", 用当前数据之前的中位数填充目前的空值.
		- If "constant", 用固定值填充目前的空值.

	fill_value: numerical value, default=0
		当 strategy='constant'时,用此参数填充nan值
	"""
	
	def __init__(self, strategy="median", fill_value=0):
		allowed_strategies = ["median", "mean", "constant"]
		if strategy not in ["median", "mean", "constant"]:
			raise ValueError("Can only use these strategies: {0} "
			                 " got strategy={1}".format(allowed_strategies,
			                                            strategy))
		self.strategy = strategy
		self.fill_value = fill_value
	
	def fit(self, X, y=None):
		"""Fit the Filler on X.
		具体的用以填nan的数据会保存在self.statistics_,可用于调用

		Parameters
		----------
		X : pd.Dataframe.

		Returns
		-------
		self : RollingNanFiller
		"""
		if self.strategy == "median":
			self.statistics_ = X.expanding(min_periods=1).median().shift(1)
		elif self.strategy == "mean":
			self.statistics_ = X.expanding(min_periods=1).mean().shift(1)
		elif self.strategy == "constant":
			self.statistics_ = self.fill_value
		return self
	
	def transform(self, X: pd.DataFrame):
		"""fill all nan in X.

		Parameters
		----------
		X : pd.Dataframe.
		"""
		check_is_fitted(self)
		statistics: Any = self.statistics_
		if self.strategy in ["median", "mean"]:
			# if X.shape != statistics.shape:
			#     raise ValueError(f"X has shape {X.shape}, expected {statistics.shape}")
			
			return X.fillna(statistics)
		
		elif self.strategy in ["constant"]:
			return X.fillna(statistics)


class clip_value(BaseEstimator, TransformerMixin):
	def __init__(self, upper_clip=0.75, lowwer_clip=0.25, n=2):
		self.upper_clip = upper_clip
		self.lowwer_clip = lowwer_clip
		self.n = n
	
	def fit(self, X, y=None):
		"""Fit the Filler on X.

		Parameters
		----------
		X : pd.Dataframe.

		Returns
		-------
		self : clip_value
		"""
		if isinstance(X, np.ndarray):
			X = pd.DataFrame(X)
		
		self.quant_75 = X.quantile(self.upper_clip)
		self.quant_25 = X.quantile(self.lowwer_clip)
		self.range_quant = self.quant_75 - self.quant_25
		self.upper_bound = self.quant_75 + self.n * self.range_quant
		self.lower_bound = self.quant_25 - self.n * self.range_quant
		for iCol in X.columns:
			X.loc[:, iCol] = np.clip(
				X.loc[:, iCol], self.lower_bound[iCol], self.upper_bound[iCol])
		return self
	
	def transform(self, X: pd.DataFrame):
		"""clip all nan in X.

		Parameters
		----------
		X : pd.Dataframe.
		"""
		if isinstance(X, np.ndarray):
			X = pd.DataFrame(X)
		X.fillna(np.nan, inplace=True)
		for iCol in X.columns:
			X.loc[:, iCol] = np.clip(
				X.loc[:, iCol], self.lower_bound[iCol], self.upper_bound[iCol])
		
		return X