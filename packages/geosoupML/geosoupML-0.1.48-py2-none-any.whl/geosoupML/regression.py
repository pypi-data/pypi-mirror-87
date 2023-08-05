from geosoup.raster import Raster, np, gdal_array, gdal
from geosoup.common import Handler, Opt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn import linear_model
from abc import ABCMeta, abstractmethod
from scipy import stats
from math import sqrt
import warnings
import pickle


__all__ = ['HRFRegressor',
           'RFRegressor',
           'MRegressor']

sep = Handler().sep


class _Regressor(object, metaclass=ABCMeta):
    """
    Regressor base class
    """

    def __init__(self,
                 data=None,
                 regressor=None,
                 **kwargs):

        self.data = data
        self.regressor = regressor
        self.features = None
        self.feature_index = None
        self.label = None
        self.output = None
        self.training_results = dict()
        self.fit = False

        self.adjustment = dict()

        if hasattr(self.regressor, 'intercept_'):
            self.intercept = self.regressor.intercept_
        else:
            self.intercept = None

        if hasattr(self.regressor, 'coef_'):
            self.coefficient = self.regressor.coef_
        else:
            self.coefficient = None

    def __repr__(self):
        return "<Regressor base class>"

    def fit_data(self,
                 data,
                 use_weights=False):
        """
        Train the regressor
        :param data: Samples object
        :param use_weights: If the sample weights provided should be used? (default: False)
        :return: None
        """
        self.data = data

        if self.regressor is not None:

            if (data.weights is None) or (not use_weights):
                self.regressor.fit(data.x, data.y)
            else:
                self.regressor.fit(data.x, data.y, data.weights)

        self.features = data.x_name
        self.label = data.y_name
        self.fit = True

    def pickle_it(self,
                  outfile):
        """
        Save regressor
        :param outfile: File to save the regressor to
        """
        outfile = Handler(filename=outfile).file_remove_check()
        with open(outfile, 'wb') as fileptr:
            pickle.dump(self, fileptr)

    @staticmethod
    def load_from_pickle(infile):
        """
        Reload regressor from file
        :param infile: File to load regressor from
        """
        with open(infile, 'rb') as fileptr:
            regressor_obj = pickle.load(fileptr)
            return regressor_obj

    def get_training_fit(self,
                         data=None,
                         regress_limit=None,
                         output_type='mean'):
        """
        Find out how well the training samples fit the model
        :param data: Samples() instance
        :param output_type: Metric to be computed from the random forest (options: 'mean','median','sd')
        :param regress_limit: List of upper and lower regression limits for training fit prediction
        :return: None
        """
        if data is None:
            data = self.data

        if self.fit:
            sample_predictions = getattr(self,
                                         'sample_predictions',
                                         None)

            if callable(sample_predictions):
                pred = sample_predictions(data,
                                          regress_limit=regress_limit,
                                          output_type=output_type)
            else:
                raise RuntimeError("Instance does not have sample_predictions() method")

            self.training_results['rsq'] = pred['rsq'] * 100.0
            self.training_results['slope'] = pred['slope']
            self.training_results['intercept'] = pred['intercept']
            self.training_results['rmse'] = pred['rmse']
        else:
            raise ValueError("Model not initialized with samples. Use fit_data() method")

    @abstractmethod
    def predict(self, *args, **kwargs):
        """
        Placeholder of subclass predict() methods
        """
        return

    @staticmethod
    def param_grid(param_dict):
        """
        Method to make list of parameters based on dictionary with parameter values
        :param param_dict:  Dictionary of parameter grid values
        :returns: List of parameter dictionaries
        """
        names = list(param_dict.keys())
        values = list(param_dict.values())
        grids = np.meshgrid(*values)
        lists = [np.array(arr).flatten() for arr in grids]

        return list(dict(zip(names, param)) for param in zip(*lists))

    @staticmethod
    def cv_result(regressor,
                  samples,
                  param_dict,
                  n_folds=5,
                  regress_limit=None,
                  output_type='mean',
                  use_weights=False,
                  adjust=True,
                  return_summary=True):
        """
        Find out how well the training samples fit the model
        :param regressor: _Regressor child class
        :param samples: data to get model fit on
        :param param_dict: Parameters dictionary for _Regressor child class
        :param n_folds: Number of folds to compute results for
        :param use_weights: If weights should be used for model fit/training
        :param adjust: If the gain and bias should be adjusted
        :param return_summary: If summary should be returned or non-summarized results
        :param output_type: Metric to be computed from the random forest (options: 'mean','median','sd')
        :param regress_limit: List of upper and lower regression limits for training fit prediction
        :return: None
        """
        regressor = regressor(data=samples,
                              **param_dict)

        folds = samples.make_folds(n_folds)

        results = []

        for trn_data, test_data in folds:
            regressor.fit_data(trn_data,
                               use_weights=use_weights)

            get_adjustment_param = getattr(regressor, 'get_adjustment_param', None)

            if adjust and (get_adjustment_param is not None) and callable(get_adjustment_param):
                get_adjustment_param(data_limits=regress_limit,
                                     output_type=output_type)

            pred = regressor.sample_predictions(test_data,
                                                regress_limit=regress_limit,
                                                output_type=output_type)
            results.append(pred)

        if not return_summary:
            return results
        else:
            _output = {'rsq_mean': np.mean([result['rsq'] for result in results]),
                       'rsq_sd': np.std([result['rsq'] for result in results]),
                       'rmse_mean': np.mean([result['rmse'] for result in results]),
                       'rmse_sd': np.std([result['rmse'] for result in results]),
                       'slope_mean': np.mean([result['slope'] for result in results]),
                       'slope_sd': np.std([result['slope'] for result in results]),
                       'intercept_mean': np.mean([result['intercept'] for result in results]),
                       'intercept_sd': np.std([result['intercept'] for result in results])}

            for fold_indx in range(n_folds):
                _output.update({'rsq_fold_{}'.format(fold_indx + 1): results[fold_indx]['rsq']})
                _output.update({'rmse_fold_{}'.format(fold_indx + 1): results[fold_indx]['rmse']})

            return _output

    def grid_search_param(self,
                          data,
                          param_dict,
                          cv_folds=5,
                          n_jobs=1,
                          select=True,
                          allowed_grad=0.1,
                          select_perc=90):
        """
        Method to search optimal parameters for the regressor. If 'select' is True, then this method
        will return a set of parameters with the best model score.
        :param data: Samples object
        :param param_dict: Dictionary of parameter grid to search for best score
        :param cv_folds: number of folds to divide the samples in
        :param n_jobs: number of parallel processes to run the grid search
        :param select: if the best set of parameters should be selected
        :param allowed_grad: max allowable percent difference between min and max score
        :param select_perc: percentile to choose for best model selection
        """

        if self.regressor is None:
            raise RuntimeError('Regressor not defined!')

        self.data = data
        self.features = data.x_name
        self.label = data.y_name

        model = GridSearchCV(self.regressor,
                             param_dict,
                             cv=cv_folds,
                             n_jobs=n_jobs)

        if data.weights is None:
            model.fit(data.x,
                      data.y)
        else:
            model.fit(data.x,
                      data.y,
                      sample_weight=data.weights)

        results = model.cv_results_

        params = results['params']
        scores_mean = results['mean_test_score']
        scores_sd = results['std_test_score']
        ranks = results['rank_test_score']

        if select:
            grad_cond = (scores_sd.max() - scores_sd.min()) / scores_sd.max() <= allowed_grad
            if not grad_cond:
                param = params[np.where(scores_mean == np.percentile(scores_mean,
                                                                     select_perc,
                                                                     interpolation='nearest'))]
            else:
                param = params[ranks.index(1)]
            return param
        else:
            return {'params': params,
                    'scores_mean': scores_mean,
                    'scores_sd': scores_sd,
                    'rank': ranks}

    @staticmethod
    def get_defaults(**kwargs):
        """
        Method to define default parameters for regressor
        :param kwargs: Keyword arguments
        """

        defaults = {
            'ulim': 0.975,
            'llim': 0.025,
            'variance_limit': 0.05,
            'min_rsq_limit': 60.0,
            'n_rand': 5,
            'uncert_dict': {},
            'half_range': True,
            'tile_size': 512,
            'n_tile_max': 5,
            'array_additive': 0.,
            'array_multiplier': 1.,
            'nodatavalue': None,
            'out_nodatavalue': None,
            'mask_band': None,
            'regressor': None,
            'output_type': 'mean',
            'band_name': 'prediction',
            'calculated_uncert_type': 'sd',
            'out_data_type': gdal.GDT_Float32,
        }

        defaults.update(kwargs)

        if 'raster' in kwargs and type(kwargs['raster']) == Raster:
            raster = kwargs['raster']

            if not raster.init:
                raster.initialize()

            nbands = raster.shape[0]
            nrows = raster.shape[1]
            ncols = raster.shape[2]

            check_bands = kwargs['check_bands'] if 'check_bands' in kwargs else list(range(nbands))
            if type(check_bands) not in (list, tuple):
                check_bands = [check_bands]

            kwargs_computed = {
                'band_multipliers': np.array([defaults['array_multiplier'] for _ in raster.bnames]),
                'band_additives': np.array([defaults['array_additive'] for _ in raster.bnames]),
                'tile_size': min([nrows, ncols]) ** 2 if (min([nrows, ncols]) ** 2) <= defaults['tile_size']
                else defaults['tile_size'],
                'out_nodatavalue': kwargs['nodatavalue'] if 'nodatavalue' in kwargs else defaults['out_nodatavalue'],
                'check_bands': check_bands,
            }

            defaults.update(kwargs_computed)

            if 'array_multiplier' in kwargs:
                if 'band_multipliers' in kwargs:
                    defaults['band_multipliers'] = np.array([defaults['band_multipliers'][elem]
                                                            if elem in defaults['band_multipliers']
                                                            else defaults['array_multiplier']
                                                            for elem in raster.bnames])
                else:
                    defaults['band_multipliers'] = np.array([defaults['array_multiplier']
                                                             for _ in raster.bnames])

            if 'array_additive' in kwargs:
                if 'band_additives' in kwargs:
                    defaults['band_additives'] = np.array([defaults['band_additives'][elem]
                                                          if elem in defaults['band_additives']
                                                          else defaults['array_additive']
                                                          for elem in raster.bnames])
                else:
                    defaults['band_additives'] = np.array([defaults['array_additive']
                                                           for _ in raster.bnames])

            if defaults['mask_band'] is not None:
                if type(defaults['mask_band']) == str:
                    try:
                        defaults['mask_band'] = raster.bnames.index(defaults['mask_band'])
                    except ValueError:
                        warnings.warn('Mask band ignored: Unrecognized band name.')
                        defaults['mask_band'] = None
                elif type(defaults['mask_band']) in (int, float):
                    if defaults['mask_band'] > raster.shape[0]:
                        warnings.warn('Mask band ignored: Mask band index greater than number of bands. ' +
                                      'Indices start at 0.')
                else:
                    warnings.warn('Mask band ignored: Unrecognized data type.')
                    defaults['mask_band'] = None

        return defaults

    @staticmethod
    def regress_raster(regressor,
                       raster_obj,
                       outfile=None,
                       outdir=None,
                       output_type='mean',
                       band_name='prediction',
                       **kwargs):
        """
        Tree variance from the RF regressor
        :param regressor: _Regressor object
        :param raster_obj: Initialized Raster object
        :param outfile: name of output file
        :param band_name: Name of the output raster band
        :param outdir: output folder
        :param output_type: standard deviation ('sd'),
                            variance ('var'),
                            median ('median'),
                            mean ('mean')
                            or confidence interval ('conf')
        :param kwargs:  array_multiplier: rescale all band arrays using this value
                        array_additive: add this value to all band arrays
                        out_data_type: output raster data type (GDAL data type)
                        nodatavalue: No data value for input raster
                        out_nodatavalue: Value to replace the input no-data value in output
                        tile_size: Number of pixels in each raster tile
                        band_additives: Values to add to each band array
                        band_multipliers: Values to scale each band array with
                        mask_band: Band to mask the pixels used in regression
                        verbose: If the steps std output should be displayed
                        uncert_dict: Dictionary with each key value pair specifying
                                     a feature band and its uncertainty band. Only
                                     one uncertainty band per feature is allowed.
        :returns: Output as raster object
        """

        nodatavalue = kwargs['nodatavalue'] if 'nodatavalue' in kwargs else 0.0

        if not raster_obj.init:
            raster_obj.initialize(nan_replacement=nodatavalue)

        if band_name is None:
            band_name = regressor.label

        kwargs.update({'out_data_type':
                       gdal_array.NumericTypeCodeToGDALTypeCode(regressor.data.y.dtype)})

        defaults = regressor.get_defaults(raster=raster_obj,
                                          output_type=output_type,
                                          band_name=band_name,
                                          **kwargs)

        verbose = defaults['verbose'] if 'verbose' in defaults else False
        defaults['verbose'] = False

        nbands = raster_obj.shape[0]
        nrows = raster_obj.shape[1]
        ncols = raster_obj.shape[2]

        # file handler object
        handler = Handler(raster_obj.name)

        # resolving output name
        if outdir is None:
            if outfile is None:
                outfile = handler.add_to_filename('_{}'.format(band_name))
        elif outfile is None:
            handler.dirname = outdir
            outfile = handler.add_to_filename('_{}'.format(band_name))
        else:
            outfile = Handler(outfile).file_remove_check()

        if regressor.feature_index is None:
            regressor.feature_index = list(raster_obj.bnames.index(feat) for feat in regressor.features)

        out_ras_arr = np.zeros([1, nrows, ncols],
                               dtype=gdal_array.GDALTypeCodeToNumericTypeCode(defaults['out_data_type']))

        if not raster_obj.tile_grid:
            raster_obj.make_tile_grid(defaults['tile_size'],
                                      defaults['tile_size'])

        if verbose:

            for k, v in defaults.items():
                Opt.cprint('{} : {}'.format(str(k), str(v)))

            Opt.cprint('\nProcessing {} raster tiles...\n'.format(str(raster_obj.ntiles)))

        count = 0
        for _, tile_arr in raster_obj.get_next_tile():

            tiept_x, tiept_y, tile_cols, tile_rows = raster_obj.tile_grid[count]['block_coords']

            if verbose:
                Opt.cprint("Processing tile {} of {}: x {}, y {}, cols {}, rows {}".format(str(count + 1),
                                                                                           str(raster_obj.ntiles),
                                                                                           str(tiept_x),
                                                                                           str(tiept_y),
                                                                                           str(tile_cols),
                                                                                           str(tile_rows)),
                           newline=' :')

            new_shape = [nbands, tile_rows * tile_cols]

            tile_arr = tile_arr.reshape(new_shape)
            tile_arr = tile_arr.swapaxes(0, 1)

            minmax = np.zeros([len(defaults['check_bands']), 2])
            bad_tile_flag = False

            for ii, band in enumerate(defaults['check_bands']):

                minmax[ii, :] = np.array([np.min(tile_arr[:, band]), np.max(tile_arr[:, band])])

                if verbose:
                    Opt.cprint(' Band {} : '.format(str(band + 1)) +
                               'min {} max {}'.format(str(minmax[ii, 0]),
                                                      str(minmax[ii, 1])),
                               newline='')

                if defaults['nodatavalue'] is not None:
                    if (minmax[ii, 0] == minmax[ii, 1] == defaults['nodatavalue']) \
                            and (band in regressor.feature_index):

                        bad_tile_flag = True

            if not bad_tile_flag:
                tile_arr_out = regressor.predict(tile_arr,
                                                 **defaults)
                if verbose:
                    Opt.cprint(' - Processed')
            else:
                tile_arr_out = np.zeros([tile_rows * tile_cols]) + defaults['out_nodatavalue']

                if verbose:
                    Opt.cprint(' - Ignored, bad tile')

            if tile_arr_out.dtype != out_ras_arr.dtype:
                tile_arr_out = tile_arr_out.astype(out_ras_arr.dtype)

            if defaults['mask_band'] is not None:
                tile_arr_out_reshaped = tile_arr_out.reshape([tile_rows, tile_cols]) * \
                                        tile_arr[defaults['mask_band'], :, :]
            else:
                tile_arr_out_reshaped = tile_arr_out.reshape([tile_rows, tile_cols])

            out_ras_arr[0, tiept_y: (tiept_y + tile_rows), tiept_x: (tiept_x + tile_cols)] = tile_arr_out_reshaped

            count += 1

        if verbose:
            Opt.cprint("\nInternal tile processing completed\n")

        out_ras = Raster(outfile)
        out_ras.dtype = defaults['out_data_type']
        out_ras.transform = raster_obj.transform
        out_ras.crs_string = raster_obj.crs_string

        out_ras.array = out_ras_arr
        out_ras.shape = [1, nrows, ncols]
        out_ras.bnames = [band_name]
        out_ras.nodatavalue = defaults['out_nodatavalue']

        # return raster object
        return out_ras

    @staticmethod
    def linear_regress(x,
                       y,
                       xlim=None,
                       ylim=None):
        """
        Calculate linear regression attributes
        :param x: Vector of independent variables 1D
        :param y: Vector of dependent variables 1D
        :param xlim: 2 element list or tuple [lower limit, upper limit]
        :param ylim: 2 element list or tuple [lower limit, upper limit]
        """
        if type(x) in (list, tuple, None):
            x_ = np.array(x)
        elif type(x) == np.ndarray:
            x_ = x.copy()
        else:
            raise ValueError('Non-array type x')

        if type(y) in (list, tuple, None):
            y_ = np.array(y)
        elif type(y) == np.ndarray:
            y_ = y.copy()
        else:
            raise ValueError('Non-array type y')

        if xlim is not None:
            exclude_loc_x = np.where((x_ < xlim[0]) & (x_ > xlim[1]))[0]
        else:
            exclude_loc_x = np.array([])

        if ylim is not None:
            exclude_loc_y = np.where((y_ < ylim[0]) & (y_ > ylim[1]))[0]
        else:
            exclude_loc_y = np.array([])

        exclude_locs = np.unique(np.hstack([exclude_loc_x, exclude_loc_y])).astype(np.int64)

        if exclude_locs.shape[0] > 0:
            mask = np.zeros(x_.shape[0], dtype=np.bool) + True
            mask[exclude_locs] = False

            x_in_limits = x_[np.where(mask)]
            y_in_limits = y_[np.where(mask)]
        else:
            x_in_limits = x_
            y_in_limits = y_

        slope, intercept, r_value, p_value, std_err = stats.linregress(x_in_limits, y_in_limits)
        rsq = r_value ** 2

        out_dict = {
            'rsq': rsq,
            'slope': slope,
            'intercept': intercept,
            'pval': p_value,
            'stderr': std_err
        }

        return out_dict


class MRegressor(_Regressor):
    """Multiple linear regressor
    This uses scikit-learn multiple regressor library
    """

    def __init__(self,
                 data=None,
                 regressor=None,
                 fit_intercept=True,
                 n_jobs=1,
                 normalize=False,
                 **kwargs):
        """
        Instantiate MRegressor class
        :param data:  Samples object
        :param regressor: Linear regressor
        :param fit_intercept: Whether to calculate the intercept for this model (default: True)
        :param n_jobs: The number of jobs to use for the computation
        :param normalize: If True, the regressors X will be normalized before regression by
                          subtracting the mean and dividing by the l2-norm
        :param kwargs: Other Key word arguments
        """
        super(MRegressor, self).__init__(data,
                                         regressor)
        if self.regressor is None:
            self.regressor = linear_model.LinearRegression(copy_X=True,
                                                           fit_intercept=fit_intercept,
                                                           n_jobs=n_jobs,
                                                           normalize=normalize)

        self.intercept = self.regressor.intercept_ if hasattr(self.regressor, 'intercept_') else None
        self.coefficients = self.regressor.coef_ if hasattr(self.regressor, 'coef_') else None

    def __repr__(self):
        """
        Representation of MRegressor instance
        """
        # gather which attributes exist
        attr_truth = [self.coefficients is not None,
                      self.intercept is not None]

        if any(attr_truth):

            print_str_list = list("Multiple Linear Regressor:\n")

            # strings to be printed for each attribute
            if attr_truth[0]:
                print_str_list.append("Coefficients: {}\n".format(', '.join([str(elem) for elem in
                                                                             self.coefficients.tolist()])))

            if attr_truth[1]:
                print_str_list.append("Intercept: {}\n".format(self.intercept))

            # combine all strings into one print string
            print_str = ''.join(print_str_list)

            return print_str

        else:
            # if empty return empty
            return "<Multiple Linear Regressor: __empty__>"

    def predict(self,
                arr,
                ntile_max=5,
                tile_size=1024,
                **kwargs):
        """
        Calculate multiple regression model prediction, variance, or standard deviation.
        Variance or standard deviation is calculated across all trees.
        Tiling is necessary in this step because large numpy arrays can cause
        memory issues during creation.

        :param arr: input numpy 2d array (axis 0: features (pixels), axis 1: bands)
        :param ntile_max: Maximum number of tiles up to which the
                          input image or array is processed without tiling (default = 9).
                          You can choose any (small) number that suits the available memory.
        :param tile_size: Size of each square tile (default = 128)
                :param kwargs: Keyword arguments:
                       'gain': Adjustment of the predicted output by linear adjustment of gain (slope)
                       'bias': Adjustment of the predicted output by linear adjustment of bias (intercept)
                       'upper_limit': Limit of maximum value of prediction
                       'lower_limit': Limit of minimum value of prediction
        :return: 1d image array (that will need reshaping if image output)
        """
        nodatavalue = None
        verbose = False

        if kwargs is not None:
            for key, value in kwargs.items():
                if key in ('gain', 'bias', 'upper_limit', 'lower_limit'):
                    self.adjustment[key] = value

                if key == 'nodatavalue':
                    nodatavalue = value

                if key == 'verbose':
                    verbose = value

        if type(arr).__name__ != 'ndarray':
            arr = np.array(arr)

        # define output array
        out_arr = np.zeros(arr.shape[0])

        # input image size
        npx_inp = int(arr.shape[0])  # number of pixels in input image
        nb_inp = int(arr.shape[1])  # number of bands in input image

        # size of tiles
        npx_tile = int(tile_size)  # pixels in each tile
        npx_last = npx_inp % npx_tile  # pixels in last tile
        ntiles = (npx_inp // npx_tile) + 1  # total tiles

        # if number of tiles in the image
        # are less than the specified number
        if ntiles > ntile_max:

            for i in range(0, ntiles - 1):
                if verbose:
                    Opt.cprint('Processing tile {} of {}'.format(str(i+1), ntiles))

                # calculate predictions for each pixel in a 2d array
                out_arr[i * npx_tile:(i + 1) * npx_tile] = \
                    self.regressor.predict(arr[i * npx_tile:(i + 1) * npx_tile, self.feature_index])

            if npx_last > 0:  # number of total pixels for the last tile

                i = ntiles - 1
                if verbose:
                    Opt.cprint('Processing tile {} of {}'.format(str(i+1), ntiles))
                out_arr[i * npx_last:(i + 1) * npx_last] = \
                    self.regressor.predict(arr[i * npx_tile:(i * npx_tile + npx_last), self.feature_index])

        else:
            out_arr = self.regressor.predict(arr[:, self.feature_index])

        if len(self.adjustment) > 0:

            if 'gain' in self.adjustment:
                out_arr = out_arr * self.adjustment['gain']

            if 'bias' in self.adjustment:
                out_arr = out_arr + self.adjustment['bias']

            if 'upper_limit' in self.adjustment:
                out_arr[out_arr > self.adjustment['upper_limit']] = self.adjustment['upper_limit']

            if 'lower_limit' in self.adjustment:
                out_arr[out_arr < self.adjustment['lower_limit']] = self.adjustment['lower_limit']

        output = out_arr

        if nodatavalue is not None:
            for ii in range(arr.shape[0]):
                output[np.unique(np.where(arr[ii, :, :] == nodatavalue)[0])] = nodatavalue

        return output

    def sample_predictions(self,
                           data,
                           **kwargs):
        """
        Get predictions from the multiple regressor
        :param data: Samples object
        """
        if 'verbose' in kwargs:
            verbose = kwargs['verbose']
        else:
            verbose = False

        self.feature_index = list(data.x_name.index(feat) for feat in self.features)

        # calculate variance of tree predictions
        prediction = self.predict(data.x,
                                  verbose=verbose)

        nan_present = np.isnan(prediction)

        if np.any(nan_present):
            non_nan_loc = np.where(~nan_present)
            prediction = prediction[non_nan_loc]
            y = data.y[non_nan_loc]
        else:
            y = data.y

        # rms error of the actual versus predicted
        rmse = sqrt(mean_squared_error(y, prediction))

        # r-squared of actual versus predicted
        lm = self.linear_regress(y, prediction)

        return {
            'pred': prediction,
            'labels': y,
            'rmse': rmse,
            'rsq': lm['rsq'],
            'slope': lm['slope'],
            'intercept': lm['intercept'],
        }

    def get_adjustment_param(self,
                             clip=0.0,
                             data_limits=None,
                             over_adjust=1.0):
        """
        get the model adjustment parameters based on training fit
        :param clip: percent of the data to be clipped from either ends to fit a constraining regression
        :param data_limits: minimum and maximum value of the output, tuple
        :param over_adjust: factor to multiply the final output with

        :return: None
        """
        if data_limits is None:
            data_limits = [self.data.y.min(), self.data.y.max()]

        regress_limit = [data_limits[0] + (clip/100.0) * (data_limits[1]-data_limits[0]),
                         data_limits[1] - (clip/100.0) * (data_limits[1]-data_limits[0])]

        self.get_training_fit(regress_limit=regress_limit)

        if self.training_results['intercept'] > regress_limit[0]:
            self.adjustment['bias'] = -1.0 * (self.training_results['intercept'] / self.training_results['slope'])

        self.adjustment['gain'] = (1.0 / self.training_results['slope']) * over_adjust

        self.adjustment['lower_limit'] = data_limits[0]
        self.adjustment['upper_limit'] = data_limits[1]


class RFRegressor(_Regressor):
    """Random Forest Regressor.
     This uses scikit-learn Random Forest regressor"""

    def __init__(self,
                 data=None,
                 regressor=None,
                 n_estimators=10,
                 min_samples_split=2,
                 min_samples_leaf=1,
                 max_depth=None,
                 max_features='auto',
                 oob_score=False,
                 criterion='mse',
                 n_jobs=1,
                 **kwargs):
        """
        Initialize RF regressor using class parameters
        :param data: Data as Samples() instance
        :param regressor: Random forest regressor
        :param n_estimators: Number of trees
        :param min_samples_split: min number of data points placed in a node before the node is split
        :param min_samples_leaf: min number of data points allowed in a leaf node
        :param max_depth: max number of levels in each decision tree of the random forest
        :param max_features: max number of features considered for splitting a node
        :param oob_score: (bool) calculate out of bag score
        :param criterion: criterion to be used (default: 'mse', options: 'mse', 'mae')
        :param n_jobs: Number of parallel processes to run the regressor on
        """

        super(RFRegressor, self).__init__(data,
                                          regressor)

        if self.regressor is None:
            self.regressor = RandomForestRegressor(n_estimators=n_estimators,
                                                   max_depth=max_depth,
                                                   min_samples_split=min_samples_split,
                                                   min_samples_leaf=min_samples_leaf,
                                                   max_features=max_features,
                                                   criterion=criterion,
                                                   oob_score=oob_score,
                                                   n_jobs=n_jobs)
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.oob_score = oob_score
        self.criterion = criterion
        self.n_jobs = n_jobs

        self.dec_paths = list()

    def __repr__(self):
        # gather which attributes exist
        attr_truth = [hasattr(self.regressor, 'estimators_'),
                      hasattr(self.regressor, 'n_features_'),
                      hasattr(self.regressor, 'n_outputs_'),
                      hasattr(self.regressor, 'oob_score_')]

        # if any exist print them
        if any(attr_truth):

            print_str_list = list("Random Forest Regressor:\n")

            # strings to be printed for each attribute
            if attr_truth[0]:
                print_str_list.append("Estimators: {}\n".format(len(self.regressor.estimators_)))

            if attr_truth[1]:
                print_str_list.append("Features: {} : {} \n".format(self.regressor.n_features_,
                                                                    ', '.join(self.features)))

            if attr_truth[2]:
                print_str_list.append("Output: {} : {} \n".format(self.regressor.n_outputs_,
                                                                  self.label))

            if attr_truth[3]:
                print_str_list.append("OOB Score: {:{w}.{p}f} %".format(self.regressor.oob_score_ * 100.0,
                                                                        w=3, p=2))

            # combine all strings into one print string
            print_str = ''.join(print_str_list)

            return print_str

        else:
            # if empty return empty
            return "<Random Forest Regressor: __empty__>"

    def regress_tile(self,
                     arr,
                     output_type='mean',
                     nodatavalue=None,
                     min_variance=None,
                     **kwargs):

        """
        Method to regress each tile of the image using one RF regressor
        :param arr: input 2D array to process (rows = elements, columns = features)
        :param output_type: Type of output to produce,
               choices: ['sd', 'var', 'full', 'mean', 'median']
               where 'sd' is for standard deviation,
               'var' is for variance
               'full is for all leaf outputs
               'median' is for median of tree outputs
               'mean' is for mean of tree outputs
        :param nodatavalue: No data value
        :param min_variance: Minimum variance after which to cutoff
        :return: numpy 1-D array
        """

        if min_variance is None:
            min_variance = 0.0  # 0.025 * (self.data.y.max() - self.data.y.min())

        # List of index of bands to be used for regression
        if 'feature_index' in kwargs:
            feature_index = np.array(kwargs['feature_index'])
        elif self.feature_index is not None:
            feature_index = np.array(self.feature_index)
        else:
            feature_index = np.array(range(0, arr.shape[0]))

        band_multipliers = np.repeat(1.0, feature_index.shape[0]) if 'band_multipliers' not in kwargs \
            else kwargs['band_multipliers']

        band_additives = np.repeat(0.0, feature_index.shape[0]) if 'band_additives' not in kwargs \
            else kwargs['band_additives']

        feat_arr = arr * \
            band_multipliers[feature_index] + \
            band_additives[feature_index]

        if nodatavalue is not None:
            mask_arr = np.apply_along_axis(lambda x: 0
                                           if np.any(x == nodatavalue) else 1,
                                           0,
                                           feat_arr)
        else:
            mask_arr = np.zeros([feat_arr.shape[0]]) + 1

        out_tile = np.zeros(feat_arr.shape[0])
        tile_arr = np.zeros([self.n_estimators, feat_arr.shape[0]])

        if output_type in ('mean', 'median', 'full'):

            # calculate tree predictions for each pixel in a 2d array
            for jj, tree_ in enumerate(self.regressor.estimators_):
                tile_arr[jj, :] = tree_.predict(feat_arr)

            if output_type == 'median':
                out_tile = np.median(tile_arr, axis=0)
            elif output_type == 'mean':
                out_tile = np.mean(tile_arr, axis=0)
            elif output_type == 'full':
                return tile_arr

        elif output_type in ('sd', 'var'):
            # Calculate variance of output across all the leaf nodes:
            # Each leaf node may have multiple samples in it.
            # We are trying to find standard deviation
            # across all leaf node samples in all the trees
            # using tree impurity statistic as we cannot access all the samples
            # once the tree is constructed.
            # Population variance is sum of between group variance and within group variance
            # read http://arxiv.org/pdf/1211.0906v2.pdf
            for jj, tree_ in enumerate(self.regressor.estimators_):
                tile_arr[jj, :] = tree_.predict(feat_arr)

                var_tree = tree_.tree_.impurity[tree_.apply(feat_arr)]  # tree/group variance

                var_tree[var_tree < min_variance] = min_variance
                mean_tree = tree_.predict(feat_arr)  # tree mean
                out_tile += var_tree + mean_tree ** 2

            predictions = np.mean(tile_arr, axis=0)  # population means

            out_tile /= len(self.regressor.estimators_)
            out_tile = out_tile - predictions ** 2.0
            out_tile[out_tile < 0.0] = 0.0

            if output_type == 'sd':
                out_tile = out_tile ** 0.5

        else:
            raise RuntimeError("Unknown output type or no output type specified."
                               "\nValid output types: mean, median, sd, var, full")

        if len(self.adjustment) > 0:

            if 'gain' in self.adjustment:
                out_tile = out_tile * self.adjustment['gain']

            if output_type not in ('sd', 'var'):

                if 'bias' in self.adjustment:
                    out_tile = out_tile + self.adjustment['bias']

                if 'upper_limit' in self.adjustment:
                    out_tile[out_tile > self.adjustment['upper_limit']] = self.adjustment['upper_limit']

                if 'lower_limit' in self.adjustment:
                    out_tile[out_tile < self.adjustment['lower_limit']] = self.adjustment['lower_limit']

        if nodatavalue is not None:
            out_tile[np.where(mask_arr == 0)] = kwargs['out_nodatavalue']

        return out_tile

    @staticmethod
    def pixel_range(regressor,
                    pixel_vec,
                    uncert_dict=None,
                    n_rand=5,
                    half_range=True,
                    output_type='mean',
                    **kwargs):
        """
        Method to compute range of regression uncertainty for each pixel
        :param pixel_vec: Input pixel vector containing feature and uncertainty bands
        :param kwargs: Additional keyword arguments to be passed on to

        :param regressor: RFRegressor object
        :param uncert_dict: Dictionary specifying the indices of
                   feature bands (keys) and their corresponding
                   uncertainty bands (values)
        :param output_type: Type of output to produce,
               choices: ['sd', 'var', 'full', 'mean', 'median']
               where 'sd' is for standard deviation,
               'var' is for variance
               'full is for all leaf outputs
               'median' is for median of tree outputs
               'mean' is for mean of tree outputs
        :param n_rand: Number of random values to generate
              in the uncertainty range (default: 5)
        :param half_range: If the input and output uncertainty values are
             - full range (x +/- a), or
             - half range (x +/- a/2)

        :return: range of uncertainty values if one or more uncertainty bands
                 are specified in uncertainty dict else returns 0
        """

        if uncert_dict is None or len(uncert_dict) == 0:
            raise RuntimeError("No uncertainty band dictionary provided")

        if type(regressor) != RFRegressor:
            raise RuntimeError("Regressor must be supplied to calculate uncertainty ranges" +
                               "Regressor must be of _Regressor class")

        n_samp = n_rand ** len(uncert_dict)

        if n_samp > 0:
            feat_arr = np.tile(pixel_vec, (n_samp, 1))

            feat_vals = pixel_vec[uncert_dict.keys()].tolist()
            uncert_vals = pixel_vec[uncert_dict.values()].tolist()

            if half_range:
                uncert_rand_lists = list((np.random.rand(n_rand) - 0.5) * uncert_val + feat_vals[ii] for
                                         ii, uncert_val in enumerate(uncert_vals))
            else:
                uncert_rand_lists = list((2 * np.random.rand(n_rand) - 1) * uncert_val + feat_vals[ii] for
                                         ii, uncert_val in enumerate(uncert_vals))

            feat_arr[:, uncert_dict.keys()] = np.array(zip(*list(np.array(temp_arr).flatten()
                                                                 for temp_arr in
                                                                 np.meshgrid(*uncert_rand_lists))))

            pred_arr = regressor.regress_tile(feat_arr,
                                              tile_start=0,
                                              tile_end=n_samp,
                                              output_type=output_type,
                                              **kwargs).flatten()

            return np.abs(pred_arr.min() - pred_arr.max())
        else:
            return

    def regress_tile_uncert(self,
                            arr,
                            output_type='mean',
                            uncert_type='sd',
                            uncert_dict=None,
                            n_rand=5,
                            half_range=True,
                            compare_uncert=False,
                            **kwargs):
        """
        Method to regress each tile of the image and compute range of uncertainty values from one RF regressor
        :param arr: input 2D array to process (rows = elements, columns = features)
        :param output_type: Type of output to produce,
               choices: ['sd', 'var', 'full', 'mean', 'median']
               where 'sd' is for standard deviation,
               'var' is for variance
               'full is for all leaf outputs
               'median' is for median of tree outputs
               'mean' is for mean of tree outputs
        :param uncert_dict: Dictionary specifying the indices of
                            feature bands (keys) and their corresponding
                            uncertainty bands (values)
        :param n_rand: Number of random values to generate in the uncertainty range (default: 5)
        :param half_range: If the input and output uncertainty values are
                             - full range (x +/- a), or
                             - half range (x +/- a/2)
        :param compare_uncert: Boolean. Compare the propagated uncertainty with
                              uncertainty in RF regression output value
                              and return the larger of the two (default: False)
        :param uncert_type: Type of value to compute as uncertainty of prediction (options: 'sd', 'var')
        :param kwargs: Keyword arguments:
                ntile_max: Maximum number of tiles up to which the
                           input image or array is processed without tiling (default = 9).
                           You can choose any (small) number that suits the available memory.
                tile_size: Number of pixels in each tile (default = 1024)
                gain: Adjustment of the predicted output by linear adjustment of gain (slope)
                bias: Adjustment of the predicted output by linear adjustment of bias (intercept)
                upper_limit: Limit of maximum value of prediction
                lower_limit: Limit of minimum value of prediction
                intvl: Prediction interval width (default: 95 percentile)
                uncert_dict: Dictionary specifying the indices of
                           feature bands (keys) and their corresponding
                           uncertainty bands (values)
                n_rand: Number of random values to generate in the uncertainty range (default: 5)
                half_range (Boolean): If the input and output uncertainty values are
                           False  - full range (x +/- a), or
                           True   - half range (x +/- a/2)
        """

        if uncert_dict is not None:
            kwargs.update({'regressor': self,
                           'uncert_dict': uncert_dict,
                           'n_rand': n_rand,
                           'output_type': output_type,
                           'half_range': half_range})

            propagated_uncert = np.apply_along_axis(self.pixel_range,
                                                    1,
                                                    arr,
                                                    **kwargs)

            if compare_uncert:
                calculated_uncert = self.regress_tile(arr,
                                                      output_type=uncert_type,
                                                      **kwargs)

                return np.apply_along_axis(lambda x: np.max(x),
                                           0,
                                           np.array([propagated_uncert, calculated_uncert]))
            else:
                return propagated_uncert
        else:
            return

    def predict(self,
                arr,
                output_type='mean',
                **kwargs):
        """
        Calculate random forest model prediction, variance, or standard deviation.
        Variance or standard deviation is calculated across all trees.
        Tiling is necessary in this step because large numpy arrays can cause
        memory issues during creation.

        :param arr: input 2d array (axis 0: features (pixels), axis 1: bands)

        :param output_type: which output to produce,
                       choices: ['sd', 'var', 'median', 'mean', 'full']
                       where 'sd' is for standard deviation,
                       'var' is for variance
                       'median' is for median of tree outputs
                       'mean' is for mean of tree outputs
                       'full' is for the full spectrum of the leaf nodes' prediction

        :param kwargs: Keyword arguments:
                        gain: Adjustment of the predicted output by linear adjustment of gain (slope)
                        bias: Adjustment of the predicted output by linear adjustment of bias (intercept)
                        upper_limit: Limit of maximum value of prediction
                        lower_limit: Limit of minimum value of prediction
                        intvl: Prediction interval width (default: 95 percentile)
                        uncert_dict: Dictionary specifying the indices of
                                   feature bands (keys) and their corresponding
                                   uncertainty bands (values)
                        n_rand: Number of random values to generate in the uncertainty range (default: 5)
                        half_range (Boolean): If the input and output uncertainty values are
                                   False  - full range (x +/- a), or
                                   True   - half range (x +/- a/2)

        :return: 1d image array (that will need reshaping if image output)
        """
        if not type(arr) == np.ndarray:
            arr = np.array(arr)

        verbose = kwargs['verbose'] if 'verbose' in kwargs else False

        kwargs.update({'output_type': output_type})

        if 'uncert_dict' in kwargs:
            uncert_dict = kwargs['uncert_dict']
        else:
            uncert_dict = None

        for key, value in kwargs.items():
            if key in ('gain', 'bias', 'upper_limit', 'lower_limit'):
                if kwargs[key] is not None:
                    self.adjustment[key] = value

        if uncert_dict is not None and type(uncert_dict) == dict and len(uncert_dict) > 0:
            out_arr = self.regress_tile_uncert(arr,
                                               **kwargs)
        else:
            out_arr = self.regress_tile(arr,
                                        **kwargs)
        if verbose:
            Opt.cprint(' min {} max {}'.format(np.min(out_arr), np.max(out_arr)))

        return out_arr

    def var_importance(self):
        """
        Return list of tuples of band names and their importance
        """

        return [(band, importance) for band, importance in
                zip(self.data.x_name, self.regressor.feature_importances_)]

    def sample_predictions(self,
                           data,
                           output_type='mean',
                           **kwargs):
        """
        Get tree predictions from the RF regressor
        :param data: Samples object
        :param output_type: Metric to be computed from RandomForestRegressor.
                           (options: 'mean','median','sd', 'var','full')
        :param kwargs: Keyword arguments:
               'gain': Adjustment of the predicted output by linear adjustment of gain (slope)
               'bias': Adjustment of the predicted output by linear adjustment of bias (intercept)
               'upper_limit': Limit of maximum value of prediction
               'lower_limit': Limit of minimum value of prediction
               'regress_limit': 2 element list of Minimum and Maximum limits of the label array [min, max]
               'all_y': Boolean (if all leaf outputs should be calculated)
               'var_y': Boolean (if variance of leaf nodes should be calculated)
               'sd_y': Boolean (if the standard dev of all values at a leaf should be calculated)
        """

        for key, value in kwargs.items():
            if key in ('gain', 'bias', 'upper_limit', 'lower_limit'):
                self.adjustment[key] = value

        if 'verbose' in kwargs:
            verbose = kwargs['verbose']
        else:
            verbose = False

        self.feature_index = list(data.x_name.index(feat) for feat in self.features)

        if 'regress_limit' in kwargs:
            regress_limit = kwargs['regress_limit']
        else:
            regress_limit = None

        prediction = self.predict(data.x,
                                  output_type=output_type,
                                  verbose=verbose)

        if regress_limit is not None:
            lm = self.linear_regress(data.y,
                                     prediction,
                                     xlim=regress_limit)
        else:
            lm = self.linear_regress(data.y,
                                     prediction)

        nan_present = np.isnan(prediction)

        if np.any(nan_present):
            non_nan_loc = np.where(~nan_present)
            prediction = prediction[non_nan_loc]
            y = data.y[non_nan_loc]
        else:
            y = data.y

        rmse = sqrt(mean_squared_error(y, prediction))

        # if outfile and pickle file are not provided,
        # then only return values
        out_dict = {
            'pred': prediction,
            'labels': data.y,
            'rmse': rmse,
            'rsq': lm['rsq'],
            'slope': lm['slope'],
            'intercept': lm['intercept'],
        }
        return out_dict

    def get_adjustment_param(self,
                             data_limits=None,
                             output_type='mean',
                             clip=0.025,
                             over_adjust=1.0):
        """
        get the model adjustment parameters based on training fit
        :param output_type: Metric to be computed from the random forest (options: 'mean','median','sd')
        :param clip: Ratio of samples not to be used at each tail end
        :param data_limits: tuple of (min, max) limits of output data
        :param over_adjust: Amount of over adjustment needed to adjust slope of the output data
        :return: None
        """

        if data_limits is None:
            data_limits = [self.data.y.min(), self.data.y.max()]

        regress_limit = [data_limits[0] + clip * (data_limits[1]-data_limits[0]),
                         data_limits[0] + (1.0-clip) * (data_limits[1]-data_limits[0])]

        self.get_training_fit(regress_limit=regress_limit,
                              output_type=output_type)

        if self.training_results['intercept'] > regress_limit[0]:
            self.adjustment['bias'] = -1.0 * (self.training_results['intercept'] / self.training_results['slope'])

        self.adjustment['gain'] = (1.0 / self.training_results['slope']) * over_adjust

        self.adjustment['lower_limit'] = data_limits[0]
        self.adjustment['upper_limit'] = data_limits[1]


class HRFRegressor(RFRegressor):

    """
    Hierarchical Random Forest Regressor.
    This class is designed to use multiple random forest regressors.
    The features in each random forest regressor must be specified.
    (based on hierarchical regression of available features)
    """

    def __init__(self,
                 data=None,
                 regressor=None,
                 **kwargs):

        super(RFRegressor, self).__init__(data,
                                          regressor)

        if regressor is not None:
            if type(regressor).__name__ not in ('list', 'tuple'):
                regressor = [regressor]

        feature_list_ = list(reg.features for reg in regressor)
        feature_index_ = list(reversed(sorted(range(len(feature_list_)),
                                              key=lambda x: len(feature_list_[x]))))

        self.features = list(feature_list_[idx] for idx in feature_index_)
        self.regressor = list(regressor[idx] for idx in feature_index_)

        if data is not None:
            if type(data).__name__ not in ('list', 'tuple'):
                data = [data]
            self.data = list(data[idx] for idx in feature_index_)
        else:
            self.data = data

        self.feature_index = None

    def __repr__(self):

        if self.regressor is None:
            repr_regressor = ['<empty>']
        elif type(self.regressor).__name__ in ('list', 'tuple'):
            repr_regressor = list(regressor.__repr__() for regressor in self.regressor)
        else:
            repr_regressor = [self.regressor.__repr__()]

        return "Hierarchical regressor object" + \
            "\n---\nRegressors: \n---\n{}".format('\n'.join(repr_regressor)) + \
            "\n---\n\n"

    def regress_raster(self,
                       raster_obj,
                       outfile=None,
                       outdir=None,
                       band_name='band_1',
                       output_type='mean',
                       array_multiplier=1.0,
                       array_additive=0.0,
                       out_data_type=gdal.GDT_Float32,
                       nodatavalue=None,
                       **kwargs):

        """Tree variance from the RF regressor
        :param raster_obj: Initialized Raster object with a 3d array
        :param outfile: name of output file
        :param array_multiplier: rescale data using this value
        :param array_additive: Rescale data using this value
        :param out_data_type: output raster data type
        :param nodatavalue: No data value for output raster
        :param band_name: Name of the output raster band
        :param outdir: output folder
        :param output_type: Should the output be standard deviation ('sd'),
                            variance ('var'), or prediction ('pred'),
                            or 'conf' for confidence interval
        :returns: Output as raster object
        """

        self.feature_index = list(list(raster_obj.bnames.index(feat) for feat in feat_grp)
                                  for feat_grp in self.features)

        return super(HRFRegressor, self).regress_raster(self,
                                                        raster_obj,
                                                        outfile=outfile,
                                                        outdir=outdir,
                                                        band_name=band_name,
                                                        output_type=output_type,
                                                        out_data_type=out_data_type,
                                                        nodatavalue=nodatavalue,
                                                        array_multiplier=array_multiplier,
                                                        array_additive=array_additive,
                                                        **kwargs)

    def predict(self,
                arr,
                output_type='mean',
                **kwargs):
        """
        Calculate random forest model prediction, variance, or standard deviation.
        Variance or standard deviation is calculated across all trees.
        Tiling is necessary in this step because large numpy arrays can cause
        memory issues during creation.

        :param arr: input 2d array (axis 0: features (pixels), axis 1: bands)

        :param output_type: which output to produce,
                       choices: ['sd', 'var', 'median', 'mean', 'full']
                       where 'sd' is for standard deviation,
                       'var' is for variance
                       'median' is for median of tree outputs
                       'mean' is for mean of tree outputs
                       'full' is for the full spectrum of the leaf nodes' prediction

        :param kwargs: Keyword arguments:
                        ntile_max: Maximum number of tiles up to which the
                                   input image or array is processed without tiling (default = 5).
                                   You can choose any (small) number that suits the available memory.
                        tile_size: Number of pixels in each tile (default = 1024)
                        gain: Adjustment of the predicted output by linear adjustment of gain (slope)
                        bias: Adjustment of the predicted output by linear adjustment of bias (intercept)
                        upper_limit: Limit of maximum value of prediction
                        lower_limit: Limit of minimum value of prediction
                        intvl: Prediction interval width (default: 95 percentile)
                        uncert_dict: Dictionary specifying the indices of
                                   feature bands (keys) and their corresponding
                                   uncertainty bands (values)
                        n_rand: Number of random values to generate in the uncertainty range (default: 5)
                        half_range (Boolean): If the input and output uncertainty values are
                                   False  - full range (x +/- a), or
                                   True   - half range (x +/- a/2)

        :return: 1d image array (that will need reshaping if image output)
        """

        if output_type == 'full':
            raise ValueError('Output type "full" is not supported for this class')

        return super(HRFRegressor, self).predict(arr,
                                                 output_type=output_type,
                                                 **kwargs)

    def regress_tile(self,
                     arr,
                     tile_start=None,
                     tile_end=None,
                     output_type='mean',
                     nodatavalue=None,
                     intvl=None,
                     min_variance=None,
                     **kwargs):

        """
        Method to regress each tile of the image with regressor hierarchy
        :param arr: input 2D array to process (rows = elements, columns = features)
        :param tile_start: pixel location of tile start
        :param tile_end: pixel location of tile end
        :param nodatavalue: No data value
        :param output_type: Type of output to produce,
                   choices: ['sd', 'var', 'full', 'mean', 'median']
                   where 'sd' is for standard deviation,
                   'var' is for variance
                   'full is for all leaf outputs
                   'median' is for median of tree outputs
                   'mean' is for mean of tree outputs
        :param intvl: Prediction interval width (default: 95 percentile)
        :param min_variance: Minimum variance after which to cutoff
        :param kwargs: Keyword arguments:
                ntile_max: Maximum number of tiles up to which the
                           input image or array is processed without tiling (default = 9).
                           You can choose any (small) number that suits the available memory.
                tile_size: Number of pixels in each tile (default = 1024)
                gain: Adjustment of the predicted output by linear adjustment of gain (slope)
                bias: Adjustment of the predicted output by linear adjustment of bias (intercept)
                upper_limit: Limit of maximum value of prediction
                lower_limit: Limit of minimum value of prediction
                intvl: Prediction interval width (default: 95 percentile)
                uncert_dict: Dictionary specifying the indices of
                           feature bands (keys) and their corresponding
                           uncertainty bands (values)
                n_rand: Number of random values to generate in the uncertainty range (default: 5)
                half_range (Boolean): If the input and output uncertainty values are
                           False  - full range (x +/- a), or
                           True   - half range (x +/- a/2)
        :return: numpy 1-D array
        """

        # leaf variance limit for sd or var output type
        if min_variance is None:
            min_variance = 0.0  # 0.025 * (self.data.y.max() - self.data.y.min())

        # define input array shape param
        if tile_end is None:
            tile_end = arr.shape[0]
        if tile_start is None:
            tile_start = 0

        # List of index of bands to be used for regression
        if 'feature_index' in kwargs:
            feature_index = kwargs['feature_index']
        elif self.feature_index is not None:
            feature_index = self.feature_index
        else:
            feature_index = np.tile(np.array(range(0, arr.shape[0])),
                                    (len(self.regressor), 1))

        # initialize output tile
        out_tile = np.zeros([tile_end - tile_start])

        # list of list of array locations where
        # all feature bands for a regressor are available for regression
        # the self.regressor list should be in decreasing order of number of feature bands
        tile_index = list()

        for ii, _ in enumerate(self.regressor):
            # array locations where all features are available for regression
            reg_index = np.where(np.apply_along_axis(lambda x: np.all(x[feature_index[ii]] != nodatavalue),
                                                     1,
                                                     arr[tile_start:tile_end, :]))[0]

            if len(tile_index) == 0:
                tile_index.append(reg_index)
            else:
                # check to see if the indices found earlier for this regressor are
                # already available for previous regressor. if so, mask them out
                for index_list in tile_index:
                    intersecting_index = np.where(np.in1d(reg_index, index_list))[0]

                    mask = np.zeros(reg_index.shape,
                                    dtype=bool) + True
                    mask[intersecting_index] = False

                    reg_index = reg_index[np.where(mask)[0]]

                # add array indices/locations not used by previous regressor to list
                tile_index.append(reg_index)

        for ii, regressor in enumerate(self.regressor):
            Opt.cprint(' . {}'.format(str(ii + 1)), newline='')

            temp_tile = np.zeros([tile_index[ii].shape[0]]) * 0.0

            if temp_tile.shape[0] > 0:

                temp_arr = (arr[tile_index[ii][:, np.newaxis] + tile_start, feature_index[ii]] *
                            kwargs['band_multipliers'][feature_index[ii]]) + \
                    kwargs['band_additives'][feature_index[ii]]

                # initialize output array for this regressor
                tile_arr = np.zeros([regressor.n_estimators, tile_index[ii].shape[0]], dtype=float)

                if output_type in ('mean', 'median'):

                    # calculate tree predictions for each pixel in the input array
                    for jj, tree_ in enumerate(regressor.regressor.estimators_):
                        tile_arr[jj, :] = tree_.predict(temp_arr)

                    if output_type == 'median':
                        temp_tile = np.median(tile_arr, axis=0)
                    elif output_type == 'mean':
                        temp_tile = np.mean(tile_arr, axis=0)

                elif output_type in ('sd', 'var'):

                    # Calculate variance of output across all the leaf nodes:
                    # Each leaf node may have multiple samples in it.
                    # We are trying to find standard deviation
                    # across all leaf node samples in all the trees
                    # using tree impurity statistic as we cannot access all the samples
                    # once the tree is constructed.
                    # Population variance is sum of between group variance and within group variance
                    # read http://arxiv.org/pdf/1211.0906v2.pdf
                    for jj, tree_ in enumerate(regressor.regressor.estimators_):
                        # predict the tree output for the tile
                        tile_arr[jj, :] = tree_.predict(temp_arr)

                        # variance in output at the leaf node of the tree
                        var_tree = tree_.tree_.impurity[tree_.apply(temp_arr)]

                        var_tree[var_tree < min_variance] = min_variance
                        mean_tree = tree_.predict(temp_arr)
                        temp_tile += var_tree + mean_tree ** 2

                    predictions = np.mean(tile_arr, axis=0)

                    temp_tile /= len(regressor.regressor.estimators_)
                    temp_tile -= predictions ** 2.0
                    temp_tile[temp_tile < 0.0] = 0.0

                    if output_type == 'sd':
                        temp_tile = temp_tile ** 0.5
                else:
                    raise RuntimeError("Unsupported output type or no output type specified")

                if len(regressor.adjustment) > 0:

                    if 'gain' in regressor.adjustment:
                        temp_tile = temp_tile * regressor.adjustment['gain']

                    if output_type not in ('sd', 'var'):

                        if 'bias' in regressor.adjustment:
                            temp_tile = temp_tile + regressor.adjustment['bias']

                        if 'upper_limit' in regressor.adjustment:
                            temp_tile[temp_tile > regressor.adjustment['upper_limit']] = \
                                regressor.adjustment['upper_limit']

                        if 'lower_limit' in regressor.adjustment:
                            temp_tile[temp_tile < regressor.adjustment['lower_limit']] = \
                                regressor.adjustment['lower_limit']

                # write output to the output tile
                out_tile[tile_index[ii]] = temp_tile

        return out_tile
