.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_tutorials2_plot_xpd_analyzer.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_tutorials2_plot_xpd_analyzer.py:

XPD Analyzer
============

This analyzer processes the x-ray powder diffraction images and yields pair distribution function data.
It is basically a wrapper of the core of the XPD server and thus its functionality is the same as the XPD server.
The only difference is that the XPD server receives data from the messages sent by a proxy
while the analyzer takes data from a database entry.
If you would like to know what the analyzer does and what input and output look like,
please see :ref:`xpd-server-functionalities`.

The sections below show how to use the XPD analyzer in Ipython.

Create an analyzer
^^^^^^^^^^^^^^^^^^

To create an ``XPDAnalyzer``, you need to create a ``XPDAnalyzerConfig`` first.
The ``XPDAnalyzerConfig`` is an object that holds the configuration of the analyzer.


.. code-block:: default


    from pdfstream.analyzers.xpd_analyzer import XPDAnalyzerConfig, XPDAnalyzer

    config = XPDAnalyzerConfig(allow_no_value=True)








The ``allow_no_value`` is an optional argument.
Please see the document of `configparser <https://docs.python.org/3/library/configparser.html>`_ for details of
the arguments.
It is the parent class of the ``XPDAnalyzerConfig``.

Then, we will load the configuration parameters into the ``config``.
We can use a .ini file, a python string or a python dictionary.


.. code-block:: default


    config.read("../source/_static/xpd_analyzer.ini")





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    ['../source/_static/xpd_analyzer.ini']



Here, we use a .ini file as an example.
The content of the file is shown below and the meaning of the parameters is described in the comments.
Please read through it and change it according to your needs.

.. include:: ../_static/xpd_analyzer.ini
   :literal:

Now, we have a ``config`` loaded with parameters.
We use it to create an analyzer.


.. code-block:: default


    analyzer = XPDAnalyzer(config)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Warning: a temporary db is created for an db. It will be destroy at the end of the session.




Get data from databroker
^^^^^^^^^^^^^^^^^^^^^^^^

The input data of the analyzer is a ``BlueskyRun``, the data entry retrieved by from a databroker catalog.
Below is an example showing the process of retrieving one run from a catalog according to its unique ID.


.. code-block:: default


    db = config.raw_db
    run = db['9d320500-b3c8-47a2-8554-ca63fa092c17']








Here, ``db`` is a databroker catalog loaded according to your configuration.
Please visit `databroker user documents <https://blueskyproject.io/databroker/v2/user/index.html>`_ for details
about what you can do with the ``db`` and ``run``.
The data inside this run is show below.


.. code-block:: default


    raw_data = run.primary.read()
    raw_data






.. raw:: html

    <div><svg style="position: absolute; width: 0; height: 0; overflow: hidden">
    <defs>
    <symbol id="icon-database" viewBox="0 0 32 32">
    <path d="M16 0c-8.837 0-16 2.239-16 5v4c0 2.761 7.163 5 16 5s16-2.239 16-5v-4c0-2.761-7.163-5-16-5z"></path>
    <path d="M16 17c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
    <path d="M16 26c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
    </symbol>
    <symbol id="icon-file-text2" viewBox="0 0 32 32">
    <path d="M28.681 7.159c-0.694-0.947-1.662-2.053-2.724-3.116s-2.169-2.030-3.116-2.724c-1.612-1.182-2.393-1.319-2.841-1.319h-15.5c-1.378 0-2.5 1.121-2.5 2.5v27c0 1.378 1.122 2.5 2.5 2.5h23c1.378 0 2.5-1.122 2.5-2.5v-19.5c0-0.448-0.137-1.23-1.319-2.841zM24.543 5.457c0.959 0.959 1.712 1.825 2.268 2.543h-4.811v-4.811c0.718 0.556 1.584 1.309 2.543 2.268zM28 29.5c0 0.271-0.229 0.5-0.5 0.5h-23c-0.271 0-0.5-0.229-0.5-0.5v-27c0-0.271 0.229-0.5 0.5-0.5 0 0 15.499-0 15.5 0v7c0 0.552 0.448 1 1 1h7v19.5z"></path>
    <path d="M23 26h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    <path d="M23 22h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    <path d="M23 18h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    </symbol>
    </defs>
    </svg>
    <style>/* CSS stylesheet for displaying xarray objects in jupyterlab.
     *
     */

    :root {
      --xr-font-color0: var(--jp-content-font-color0, rgba(0, 0, 0, 1));
      --xr-font-color2: var(--jp-content-font-color2, rgba(0, 0, 0, 0.54));
      --xr-font-color3: var(--jp-content-font-color3, rgba(0, 0, 0, 0.38));
      --xr-border-color: var(--jp-border-color2, #e0e0e0);
      --xr-disabled-color: var(--jp-layout-color3, #bdbdbd);
      --xr-background-color: var(--jp-layout-color0, white);
      --xr-background-color-row-even: var(--jp-layout-color1, white);
      --xr-background-color-row-odd: var(--jp-layout-color2, #eeeeee);
    }

    html[theme=dark],
    body.vscode-dark {
      --xr-font-color0: rgba(255, 255, 255, 1);
      --xr-font-color2: rgba(255, 255, 255, 0.54);
      --xr-font-color3: rgba(255, 255, 255, 0.38);
      --xr-border-color: #1F1F1F;
      --xr-disabled-color: #515151;
      --xr-background-color: #111111;
      --xr-background-color-row-even: #111111;
      --xr-background-color-row-odd: #313131;
    }

    .xr-wrap {
      display: block;
      min-width: 300px;
      max-width: 700px;
    }

    .xr-text-repr-fallback {
      /* fallback to plain text repr when CSS is not injected (untrusted notebook) */
      display: none;
    }

    .xr-header {
      padding-top: 6px;
      padding-bottom: 6px;
      margin-bottom: 4px;
      border-bottom: solid 1px var(--xr-border-color);
    }

    .xr-header > div,
    .xr-header > ul {
      display: inline;
      margin-top: 0;
      margin-bottom: 0;
    }

    .xr-obj-type,
    .xr-array-name {
      margin-left: 2px;
      margin-right: 10px;
    }

    .xr-obj-type {
      color: var(--xr-font-color2);
    }

    .xr-sections {
      padding-left: 0 !important;
      display: grid;
      grid-template-columns: 150px auto auto 1fr 20px 20px;
    }

    .xr-section-item {
      display: contents;
    }

    .xr-section-item input {
      display: none;
    }

    .xr-section-item input + label {
      color: var(--xr-disabled-color);
    }

    .xr-section-item input:enabled + label {
      cursor: pointer;
      color: var(--xr-font-color2);
    }

    .xr-section-item input:enabled + label:hover {
      color: var(--xr-font-color0);
    }

    .xr-section-summary {
      grid-column: 1;
      color: var(--xr-font-color2);
      font-weight: 500;
    }

    .xr-section-summary > span {
      display: inline-block;
      padding-left: 0.5em;
    }

    .xr-section-summary-in:disabled + label {
      color: var(--xr-font-color2);
    }

    .xr-section-summary-in + label:before {
      display: inline-block;
      content: '►';
      font-size: 11px;
      width: 15px;
      text-align: center;
    }

    .xr-section-summary-in:disabled + label:before {
      color: var(--xr-disabled-color);
    }

    .xr-section-summary-in:checked + label:before {
      content: '▼';
    }

    .xr-section-summary-in:checked + label > span {
      display: none;
    }

    .xr-section-summary,
    .xr-section-inline-details {
      padding-top: 4px;
      padding-bottom: 4px;
    }

    .xr-section-inline-details {
      grid-column: 2 / -1;
    }

    .xr-section-details {
      display: none;
      grid-column: 1 / -1;
      margin-bottom: 5px;
    }

    .xr-section-summary-in:checked ~ .xr-section-details {
      display: contents;
    }

    .xr-array-wrap {
      grid-column: 1 / -1;
      display: grid;
      grid-template-columns: 20px auto;
    }

    .xr-array-wrap > label {
      grid-column: 1;
      vertical-align: top;
    }

    .xr-preview {
      color: var(--xr-font-color3);
    }

    .xr-array-preview,
    .xr-array-data {
      padding: 0 5px !important;
      grid-column: 2;
    }

    .xr-array-data,
    .xr-array-in:checked ~ .xr-array-preview {
      display: none;
    }

    .xr-array-in:checked ~ .xr-array-data,
    .xr-array-preview {
      display: inline-block;
    }

    .xr-dim-list {
      display: inline-block !important;
      list-style: none;
      padding: 0 !important;
      margin: 0;
    }

    .xr-dim-list li {
      display: inline-block;
      padding: 0;
      margin: 0;
    }

    .xr-dim-list:before {
      content: '(';
    }

    .xr-dim-list:after {
      content: ')';
    }

    .xr-dim-list li:not(:last-child):after {
      content: ',';
      padding-right: 5px;
    }

    .xr-has-index {
      font-weight: bold;
    }

    .xr-var-list,
    .xr-var-item {
      display: contents;
    }

    .xr-var-item > div,
    .xr-var-item label,
    .xr-var-item > .xr-var-name span {
      background-color: var(--xr-background-color-row-even);
      margin-bottom: 0;
    }

    .xr-var-item > .xr-var-name:hover span {
      padding-right: 5px;
    }

    .xr-var-list > li:nth-child(odd) > div,
    .xr-var-list > li:nth-child(odd) > label,
    .xr-var-list > li:nth-child(odd) > .xr-var-name span {
      background-color: var(--xr-background-color-row-odd);
    }

    .xr-var-name {
      grid-column: 1;
    }

    .xr-var-dims {
      grid-column: 2;
    }

    .xr-var-dtype {
      grid-column: 3;
      text-align: right;
      color: var(--xr-font-color2);
    }

    .xr-var-preview {
      grid-column: 4;
    }

    .xr-var-name,
    .xr-var-dims,
    .xr-var-dtype,
    .xr-preview,
    .xr-attrs dt {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      padding-right: 10px;
    }

    .xr-var-name:hover,
    .xr-var-dims:hover,
    .xr-var-dtype:hover,
    .xr-attrs dt:hover {
      overflow: visible;
      width: auto;
      z-index: 1;
    }

    .xr-var-attrs,
    .xr-var-data {
      display: none;
      background-color: var(--xr-background-color) !important;
      padding-bottom: 5px !important;
    }

    .xr-var-attrs-in:checked ~ .xr-var-attrs,
    .xr-var-data-in:checked ~ .xr-var-data {
      display: block;
    }

    .xr-var-data > table {
      float: right;
    }

    .xr-var-name span,
    .xr-var-data,
    .xr-attrs {
      padding-left: 25px !important;
    }

    .xr-attrs,
    .xr-var-attrs,
    .xr-var-data {
      grid-column: 1 / -1;
    }

    dl.xr-attrs {
      padding: 0;
      margin: 0;
      display: grid;
      grid-template-columns: 125px auto;
    }

    .xr-attrs dt, dd {
      padding: 0;
      margin: 0;
      float: left;
      padding-right: 10px;
      width: auto;
    }

    .xr-attrs dt {
      font-weight: normal;
      grid-column: 1;
    }

    .xr-attrs dt:hover span {
      display: inline-block;
      background: var(--xr-background-color);
      padding-right: 10px;
    }

    .xr-attrs dd {
      grid-column: 2;
      white-space: pre-wrap;
      word-break: break-all;
    }

    .xr-icon-database,
    .xr-icon-file-text2 {
      display: inline-block;
      vertical-align: middle;
      width: 1em;
      height: 1.5em !important;
      stroke-width: 0;
      stroke: currentColor;
      fill: currentColor;
    }
    </style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt;
    Dimensions:                              (dim_0: 1, dim_1: 2048, dim_10: 2, dim_2: 2048, dim_3: 17, dim_4: 3, dim_5: 40, dim_6: 2, dim_7: 19, dim_8: 3, dim_9: 14, time: 1)
    Coordinates:
      * time                                 (time) float64 1.582e+09
    Dimensions without coordinates: dim_0, dim_1, dim_10, dim_2, dim_3, dim_4, dim_5, dim_6, dim_7, dim_8, dim_9
    Data variables:
        pe1_image                            (time, dim_0, dim_1, dim_2) uint16 0...
        pe1_stats1_total                     (time) float64 4.41e+08
        pe1:pe1_cam_acquire_period           (time) float64 0.1
        pe1:pe1_cam_acquire_time             (time) float64 0.2
        pe1:pe1_cam_bin_x                    (time) int64 1
        pe1:pe1_cam_bin_y                    (time) int64 1
        pe1:pe1_cam_image_mode               (time) int64 2
        pe1:pe1_cam_manufacturer             (time) &lt;U12 &#x27;Perkin Elmer&#x27;
        pe1:pe1_cam_model                    (time) &lt;U23 &#x27;XRD [0820/1620/1621] xN&#x27;
        pe1:pe1_cam_num_exposures            (time) int64 1
        pe1:pe1_cam_trigger_mode             (time) int64 0
        pe1:pe1_tiff_configuration_names     (time, dim_3) &lt;U29 &#x27;pe1_tiff_configu...
        pe1:pe1_tiff_port_name               (time) &lt;U9 &#x27;FileTIFF1&#x27;
        pe1:pe1_tiff_asyn_pipeline_config    (time, dim_4) &lt;U28 &#x27;pe1_cam_configur...
        pe1:pe1_tiff_blocking_callbacks      (time) &lt;U3 &#x27;Yes&#x27;
        pe1:pe1_tiff_enable                  (time) &lt;U6 &#x27;Enable&#x27;
        pe1:pe1_tiff_nd_array_port           (time) &lt;U5 &#x27;PROC1&#x27;
        pe1:pe1_tiff_plugin_type             (time) &lt;U10 &#x27;NDFileTIFF&#x27;
        pe1:pe1_tiff_auto_increment          (time) int64 1
        pe1:pe1_tiff_auto_save               (time) int64 0
        pe1:pe1_tiff_file_format             (time) int64 0
        pe1:pe1_tiff_file_name               (time) &lt;U23 &#x27;92b6b929-d904-42f4-9017&#x27;
        pe1:pe1_tiff_file_path               (time) &lt;U23 &#x27;G:\\pe1_data\\2020\\02\...
        pe1:pe1_tiff_file_path_exists        (time) int64 1
        pe1:pe1_tiff_file_template           (time) &lt;U15 &#x27;%s%s_%6.6d.tiff&#x27;
        pe1:pe1_tiff_file_write_mode         (time) int64 1
        pe1:pe1_tiff_full_file_name          (time) &lt;U58 &#x27;G:\\pe1_data\\2020\\02\...
        pe1:pe1_tiff_num_capture             (time) int64 1
        pe1:pe1_proc_configuration_names     (time, dim_5) &lt;U29 &#x27;pe1_proc_configu...
        pe1:pe1_proc_port_name               (time) &lt;U5 &#x27;PROC1&#x27;
        pe1:pe1_proc_asyn_pipeline_config    (time, dim_6) &lt;U28 &#x27;pe1_cam_configur...
        pe1:pe1_proc_blocking_callbacks      (time) &lt;U3 &#x27;Yes&#x27;
        pe1:pe1_proc_data_type               (time) &lt;U6 &#x27;UInt16&#x27;
        pe1:pe1_proc_enable                  (time) &lt;U6 &#x27;Enable&#x27;
        pe1:pe1_proc_nd_array_port           (time) &lt;U6 &#x27;PEDET1&#x27;
        pe1:pe1_proc_plugin_type             (time) &lt;U15 &#x27;NDPluginProcess&#x27;
        pe1:pe1_proc_auto_offset_scale       (time) &lt;U4 &#x27;Done&#x27;
        pe1:pe1_proc_auto_reset_filter       (time) &lt;U3 &#x27;Yes&#x27;
        pe1:pe1_proc_copy_to_filter_seq      (time) int64 0
        pe1:pe1_proc_data_type_out           (time) &lt;U9 &#x27;Automatic&#x27;
        pe1:pe1_proc_difference_seq          (time) int64 0
        pe1:pe1_proc_enable_background       (time) &lt;U7 &#x27;Disable&#x27;
        pe1:pe1_proc_enable_filter           (time) &lt;U6 &#x27;Enable&#x27;
        pe1:pe1_proc_enable_flat_field       (time) &lt;U7 &#x27;Disable&#x27;
        pe1:pe1_proc_enable_high_clip        (time) &lt;U7 &#x27;Disable&#x27;
        pe1:pe1_proc_enable_low_clip         (time) &lt;U7 &#x27;Disable&#x27;
        pe1:pe1_proc_enable_offset_scale     (time) &lt;U7 &#x27;Disable&#x27;
        pe1:pe1_proc_foffset                 (time) float64 0.0
        pe1:pe1_proc_fscale                  (time) float64 1.0
        pe1:pe1_proc_filter_callbacks        (time) &lt;U12 &#x27;Array N only&#x27;
        pe1:pe1_proc_filter_type             (time) &lt;U7 &#x27;Average&#x27;
        pe1:pe1_proc_filter_type_seq         (time) int64 0
        pe1:pe1_proc_high_clip               (time) float64 100.0
        pe1:pe1_proc_low_clip                (time) float64 0.0
        pe1:pe1_proc_num_filter              (time) int64 50
        pe1:pe1_proc_num_filter_recip        (time) float64 0.02
        pe1:pe1_proc_num_filtered            (time) int64 2
        pe1:pe1_proc_o_offset                (time) float64 0.0
        pe1:pe1_proc_o_scale                 (time) float64 1.0
        pe1:pe1_proc_offset                  (time) float64 0.0
        pe1:pe1_proc_roffset                 (time) float64 0.0
        pe1:pe1_proc_scale                   (time) float64 1.0
        pe1:pe1_proc_scale_flat_field        (time) float64 255.0
        pe1:pe1_proc_valid_background        (time) &lt;U7 &#x27;Invalid&#x27;
        pe1:pe1_proc_valid_flat_field        (time) &lt;U7 &#x27;Invalid&#x27;
        pe1:pe1_images_per_set               (time) float64 50.0
        pe1:pe1_number_of_sets               (time) int64 1
        pe1:pe1_pixel_size                   (time) float64 0.0002
        pe1:pe1_detector_type                (time) &lt;U6 &#x27;Perkin&#x27;
        pe1:pe1_stats1_configuration_names   (time, dim_7) &lt;U31 &#x27;pe1_stats1_confi...
        pe1:pe1_stats1_port_name             (time) &lt;U6 &#x27;STATS1&#x27;
        pe1:pe1_stats1_asyn_pipeline_config  (time, dim_8) &lt;U30 &#x27;pe1_cam_configur...
        pe1:pe1_stats1_blocking_callbacks    (time) &lt;U3 &#x27;Yes&#x27;
        pe1:pe1_stats1_enable                (time) &lt;U6 &#x27;Enable&#x27;
        pe1:pe1_stats1_nd_array_port         (time) &lt;U4 &#x27;ROI1&#x27;
        pe1:pe1_stats1_plugin_type           (time) &lt;U13 &#x27;NDPluginStats&#x27;
        pe1:pe1_stats1_bgd_width             (time) int64 1
        pe1:pe1_stats1_centroid_threshold    (time) float64 1.0
        pe1:pe1_stats1_compute_centroid      (time) &lt;U2 &#x27;No&#x27;
        pe1:pe1_stats1_compute_histogram     (time) &lt;U2 &#x27;No&#x27;
        pe1:pe1_stats1_compute_profiles      (time) &lt;U2 &#x27;No&#x27;
        pe1:pe1_stats1_compute_statistics    (time) &lt;U3 &#x27;Yes&#x27;
        pe1:pe1_stats1_hist_max              (time) float64 255.0
        pe1:pe1_stats1_hist_min              (time) float64 0.0
        pe1:pe1_stats1_hist_size             (time) int64 256
        pe1:pe1_stats1_ts_num_points         (time) int64 2048
        pe1:pe1_roi1_configuration_names     (time, dim_9) &lt;U29 &#x27;pe1_roi1_configu...
        pe1:pe1_roi1_port_name               (time) &lt;U4 &#x27;ROI1&#x27;
        pe1:pe1_roi1_asyn_pipeline_config    (time, dim_10) &lt;U28 &#x27;pe1_cam_configu...
        pe1:pe1_roi1_blocking_callbacks      (time) &lt;U3 &#x27;Yes&#x27;
        pe1:pe1_roi1_enable                  (time) &lt;U6 &#x27;Enable&#x27;
        pe1:pe1_roi1_nd_array_port           (time) &lt;U6 &#x27;PEDET1&#x27;
        pe1:pe1_roi1_plugin_type             (time) &lt;U11 &#x27;NDPluginROI&#x27;
        pe1:pe1_roi1_data_type_out           (time) &lt;U9 &#x27;Automatic&#x27;
        pe1:pe1_roi1_enable_scale            (time) &lt;U7 &#x27;Disable&#x27;
        pe1:pe1_roi1_name_                   (time) &lt;U1 &#x27;&#x27;
        seq_num                              (time) int64 1
        uid                                  (time) &lt;U36 &#x27;ad3b7a7f-6564-4157-933f...</pre><div class='xr-wrap' hidden><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-97f80205-a3bf-47a5-8022-11ac49511987' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-97f80205-a3bf-47a5-8022-11ac49511987' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span>dim_0</span>: 1</li><li><span>dim_1</span>: 2048</li><li><span>dim_10</span>: 2</li><li><span>dim_2</span>: 2048</li><li><span>dim_3</span>: 17</li><li><span>dim_4</span>: 3</li><li><span>dim_5</span>: 40</li><li><span>dim_6</span>: 2</li><li><span>dim_7</span>: 19</li><li><span>dim_8</span>: 3</li><li><span>dim_9</span>: 14</li><li><span class='xr-has-index'>time</span>: 1</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-023dd6a7-258a-4fb6-9cef-739cf3cf1193' class='xr-section-summary-in' type='checkbox'  checked><label for='section-023dd6a7-258a-4fb6-9cef-739cf3cf1193' class='xr-section-summary' >Coordinates: <span>(1)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.582e+09</div><input id='attrs-94acd664-b31f-45e7-b8ab-ce4bc85c4a08' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-94acd664-b31f-45e7-b8ab-ce4bc85c4a08' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8b773131-6db5-4b48-906c-361ebc8d0172' class='xr-var-data-in' type='checkbox'><label for='data-8b773131-6db5-4b48-906c-361ebc8d0172' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.581814e+09])</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-ab1072bd-3e76-4bb7-8d90-4411a61340d9' class='xr-section-summary-in' type='checkbox'  ><label for='section-ab1072bd-3e76-4bb7-8d90-4411a61340d9' class='xr-section-summary' >Data variables: <span>(98)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>pe1_image</span></div><div class='xr-var-dims'>(time, dim_0, dim_1, dim_2)</div><div class='xr-var-dtype'>uint16</div><div class='xr-var-preview xr-preview'>0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0</div><input id='attrs-464d63a8-dc11-4b91-a6b1-a2f888393970' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-464d63a8-dc11-4b91-a6b1-a2f888393970' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-75a29549-c44f-4d96-a36d-208f50381c2a' class='xr-var-data-in' type='checkbox'><label for='data-75a29549-c44f-4d96-a36d-208f50381c2a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[[   0,    0,    0, ...,    0,    0,    0],
             [4594, 4576, 4587, ..., 4123, 4172, 4122],
             [4635, 4600, 4624, ..., 4318, 4231, 4216],
             ...,
             [4335, 4315, 4312, ..., 4540, 4511, 4529],
             [4229, 4257, 4251, ..., 4458, 4474, 4525],
             [   0,    0,    0, ...,    0,    0,    0]]]], dtype=uint16)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1_stats1_total</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>4.41e+08</div><input id='attrs-c1a0ed05-c311-4fd5-9c7a-24d36bcfde02' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c1a0ed05-c311-4fd5-9c7a-24d36bcfde02' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-88b8c5d6-b1f2-4343-8766-dce4dde3c0bb' class='xr-var-data-in' type='checkbox'><label for='data-88b8c5d6-b1f2-4343-8766-dce4dde3c0bb' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([4.41031435e+08])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_acquire_period</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.1</div><input id='attrs-9bcb13fa-a960-40d2-b50b-d210bcb11f43' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9bcb13fa-a960-40d2-b50b-d210bcb11f43' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b8cf1bdf-6f9a-4408-b764-703e5e7911f3' class='xr-var-data-in' type='checkbox'><label for='data-b8cf1bdf-6f9a-4408-b764-703e5e7911f3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_acquire_time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.2</div><input id='attrs-89a304a2-1ee2-42de-8ae7-9ed00a64eaf4' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-89a304a2-1ee2-42de-8ae7-9ed00a64eaf4' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d66ab382-7c53-40cd-919c-c9141f16dac9' class='xr-var-data-in' type='checkbox'><label for='data-d66ab382-7c53-40cd-919c-c9141f16dac9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.2])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_bin_x</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-9b54847f-df67-4646-8a4c-9779b7437666' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9b54847f-df67-4646-8a4c-9779b7437666' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f002f7e4-654c-45a7-b346-8569dc449341' class='xr-var-data-in' type='checkbox'><label for='data-f002f7e4-654c-45a7-b346-8569dc449341' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_bin_y</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-6f2bd19b-86e7-4c29-9f85-62050b935d3d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6f2bd19b-86e7-4c29-9f85-62050b935d3d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b987240f-3b81-46f7-9f2d-a0be7187631f' class='xr-var-data-in' type='checkbox'><label for='data-b987240f-3b81-46f7-9f2d-a0be7187631f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_image_mode</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>2</div><input id='attrs-c3bee9bb-8d6d-4544-b7da-2bc2289bdd29' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c3bee9bb-8d6d-4544-b7da-2bc2289bdd29' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3e189e37-32ac-4875-930b-2a3884ce844b' class='xr-var-data-in' type='checkbox'><label for='data-3e189e37-32ac-4875-930b-2a3884ce844b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([2])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_manufacturer</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U12</div><div class='xr-var-preview xr-preview'>&#x27;Perkin Elmer&#x27;</div><input id='attrs-934a2e65-1978-4f3c-9323-8e563bf5883e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-934a2e65-1978-4f3c-9323-8e563bf5883e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-956c4731-765d-48a1-8206-e7db227cdb98' class='xr-var-data-in' type='checkbox'><label for='data-956c4731-765d-48a1-8206-e7db227cdb98' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Perkin Elmer&#x27;], dtype=&#x27;&lt;U12&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_model</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U23</div><div class='xr-var-preview xr-preview'>&#x27;XRD [0820/1620/1621] xN&#x27;</div><input id='attrs-214a66a2-d2c9-42b2-abdc-e7c046543685' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-214a66a2-d2c9-42b2-abdc-e7c046543685' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ac3f374b-412d-4d7e-9b33-b37532369f71' class='xr-var-data-in' type='checkbox'><label for='data-ac3f374b-412d-4d7e-9b33-b37532369f71' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;XRD [0820/1620/1621] xN&#x27;], dtype=&#x27;&lt;U23&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_num_exposures</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-a437b851-4c1a-41fe-a42b-ef752b66a284' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a437b851-4c1a-41fe-a42b-ef752b66a284' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-aea7418e-6ccb-4d09-be8e-f6c9089f68a3' class='xr-var-data-in' type='checkbox'><label for='data-aea7418e-6ccb-4d09-be8e-f6c9089f68a3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_trigger_mode</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-d9242552-2501-4a02-b6cf-e4267148cf2f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-d9242552-2501-4a02-b6cf-e4267148cf2f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-91192ed9-6cd9-4c87-bc2c-923ff44d9168' class='xr-var-data-in' type='checkbox'><label for='data-91192ed9-6cd9-4c87-bc2c-923ff44d9168' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_configuration_names</span></div><div class='xr-var-dims'>(time, dim_3)</div><div class='xr-var-dtype'>&lt;U29</div><div class='xr-var-preview xr-preview'>&#x27;pe1_tiff_configuration_names&#x27; ....</div><input id='attrs-0f788d1d-844e-4fea-a7b8-ccd6d81b0d58' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0f788d1d-844e-4fea-a7b8-ccd6d81b0d58' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fa67d8b8-bc2c-4cf8-aa2d-c9df992c3faf' class='xr-var-data-in' type='checkbox'><label for='data-fa67d8b8-bc2c-4cf8-aa2d-c9df992c3faf' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_tiff_configuration_names&#x27;, &#x27;pe1_tiff_port_name&#x27;,
            &#x27;pe1_tiff_asyn_pipeline_config&#x27;, &#x27;pe1_tiff_blocking_callbacks&#x27;,
            &#x27;pe1_tiff_enable&#x27;, &#x27;pe1_tiff_nd_array_port&#x27;,
            &#x27;pe1_tiff_plugin_type&#x27;, &#x27;pe1_tiff_auto_increment&#x27;,
            &#x27;pe1_tiff_auto_save&#x27;, &#x27;pe1_tiff_file_format&#x27;,
            &#x27;pe1_tiff_file_name&#x27;, &#x27;pe1_tiff_file_path&#x27;,
            &#x27;pe1_tiff_file_path_exists&#x27;, &#x27;pe1_tiff_file_template&#x27;,
            &#x27;pe1_tiff_file_write_mode&#x27;, &#x27;pe1_tiff_full_file_name&#x27;,
            &#x27;pe1_tiff_num_capture&#x27;]], dtype=&#x27;&lt;U29&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>&#x27;FileTIFF1&#x27;</div><input id='attrs-e81728dd-d7bb-4419-bf7a-6dca5c79c48b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e81728dd-d7bb-4419-bf7a-6dca5c79c48b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ed973cdb-9680-4927-a5c5-a2554228f7c3' class='xr-var-data-in' type='checkbox'><label for='data-ed973cdb-9680-4927-a5c5-a2554228f7c3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;FileTIFF1&#x27;], dtype=&#x27;&lt;U9&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_4)</div><div class='xr-var-dtype'>&lt;U28</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; .....</div><input id='attrs-c5c244e9-08a6-43fc-b9e2-cbe69c67088e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c5c244e9-08a6-43fc-b9e2-cbe69c67088e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b8d769f2-a271-427b-9e37-e6541cb0324f' class='xr-var-data-in' type='checkbox'><label for='data-b8d769f2-a271-427b-9e37-e6541cb0324f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_proc_configuration_names&#x27;,
            &#x27;pe1_tiff_configuration_names&#x27;]], dtype=&#x27;&lt;U28&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-54cd8d1b-107a-4182-92d9-560135810ff5' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-54cd8d1b-107a-4182-92d9-560135810ff5' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-661cc3e1-c88d-4c9f-96e1-fc5a06bc65bb' class='xr-var-data-in' type='checkbox'><label for='data-661cc3e1-c88d-4c9f-96e1-fc5a06bc65bb' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-ea76cd04-6baf-4ae1-9672-306129acbb86' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ea76cd04-6baf-4ae1-9672-306129acbb86' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3499bab5-8da9-498d-85ed-7574dab24a33' class='xr-var-data-in' type='checkbox'><label for='data-3499bab5-8da9-498d-85ed-7574dab24a33' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U5</div><div class='xr-var-preview xr-preview'>&#x27;PROC1&#x27;</div><input id='attrs-b5d0092b-7e78-4fee-b9d2-bdce79ca73cb' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b5d0092b-7e78-4fee-b9d2-bdce79ca73cb' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9ca0617a-8c36-4cd5-b0d7-550106c929a5' class='xr-var-data-in' type='checkbox'><label for='data-9ca0617a-8c36-4cd5-b0d7-550106c929a5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PROC1&#x27;], dtype=&#x27;&lt;U5&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U10</div><div class='xr-var-preview xr-preview'>&#x27;NDFileTIFF&#x27;</div><input id='attrs-02035d5f-e866-42e8-8d32-f1a235019f64' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-02035d5f-e866-42e8-8d32-f1a235019f64' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-42ae4abd-665c-499a-a7bf-261a3864c80b' class='xr-var-data-in' type='checkbox'><label for='data-42ae4abd-665c-499a-a7bf-261a3864c80b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDFileTIFF&#x27;], dtype=&#x27;&lt;U10&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_auto_increment</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-35e18cf4-5bf2-4a49-a71c-d2c0dc658dcb' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-35e18cf4-5bf2-4a49-a71c-d2c0dc658dcb' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5207232a-d8e6-445d-bfa4-1e6051ed8b0a' class='xr-var-data-in' type='checkbox'><label for='data-5207232a-d8e6-445d-bfa4-1e6051ed8b0a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_auto_save</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-7191aeed-fdc3-46b5-b07c-5a943b0ff907' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7191aeed-fdc3-46b5-b07c-5a943b0ff907' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-61368491-3207-4258-8797-aa94d09e18f1' class='xr-var-data-in' type='checkbox'><label for='data-61368491-3207-4258-8797-aa94d09e18f1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_format</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-40e0c69b-1779-429e-b0a0-69812e4271ce' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-40e0c69b-1779-429e-b0a0-69812e4271ce' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7bac51f1-1157-4e90-ba49-9cd249c93fc8' class='xr-var-data-in' type='checkbox'><label for='data-7bac51f1-1157-4e90-ba49-9cd249c93fc8' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U23</div><div class='xr-var-preview xr-preview'>&#x27;92b6b929-d904-42f4-9017&#x27;</div><input id='attrs-349a7b66-bec6-45be-8e04-c6f7a842f07e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-349a7b66-bec6-45be-8e04-c6f7a842f07e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a0e015ea-1541-4890-9aca-3b1dab086ad9' class='xr-var-data-in' type='checkbox'><label for='data-a0e015ea-1541-4890-9aca-3b1dab086ad9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;92b6b929-d904-42f4-9017&#x27;], dtype=&#x27;&lt;U23&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_path</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U23</div><div class='xr-var-preview xr-preview'>&#x27;G:\\pe1_data\\2020\\02\\15\\&#x27;</div><input id='attrs-f7ab0007-e4c0-492b-8600-2aa4807f16ef' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f7ab0007-e4c0-492b-8600-2aa4807f16ef' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c8175109-62db-465e-ba78-5183e3e7b557' class='xr-var-data-in' type='checkbox'><label for='data-c8175109-62db-465e-ba78-5183e3e7b557' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;G:\\pe1_data\\2020\\02\\15\\&#x27;], dtype=&#x27;&lt;U23&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_path_exists</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-8c19dab1-e250-4090-868f-927b65285c82' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8c19dab1-e250-4090-868f-927b65285c82' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c3e86400-33bd-4eda-9957-af4e8fce7025' class='xr-var-data-in' type='checkbox'><label for='data-c3e86400-33bd-4eda-9957-af4e8fce7025' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_template</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U15</div><div class='xr-var-preview xr-preview'>&#x27;%s%s_%6.6d.tiff&#x27;</div><input id='attrs-850a7326-a698-4e28-bc0e-65762929c3a9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-850a7326-a698-4e28-bc0e-65762929c3a9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-320bef0c-3df9-4a79-bcfa-cc8c4ef7d2b1' class='xr-var-data-in' type='checkbox'><label for='data-320bef0c-3df9-4a79-bcfa-cc8c4ef7d2b1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;%s%s_%6.6d.tiff&#x27;], dtype=&#x27;&lt;U15&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_write_mode</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-5b9446e1-ebf6-47eb-a941-032ca5f5db2c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5b9446e1-ebf6-47eb-a941-032ca5f5db2c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-51ff5329-541f-4ba6-8a99-317537eeeab3' class='xr-var-data-in' type='checkbox'><label for='data-51ff5329-541f-4ba6-8a99-317537eeeab3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_full_file_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U58</div><div class='xr-var-preview xr-preview'>&#x27;G:\\pe1_data\\2020\\02\\15\\92b...</div><input id='attrs-db979bb7-3905-48e1-8bcd-87433af030b2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-db979bb7-3905-48e1-8bcd-87433af030b2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-49884de4-3357-4c5e-918a-7fd9ec17a75d' class='xr-var-data-in' type='checkbox'><label for='data-49884de4-3357-4c5e-918a-7fd9ec17a75d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;G:\\pe1_data\\2020\\02\\15\\92b6b929-d904-42f4-9017_000000.tiff&#x27;],
          dtype=&#x27;&lt;U58&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_num_capture</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-9ba35328-8868-4b9a-941e-582a7df73034' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9ba35328-8868-4b9a-941e-582a7df73034' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-db12c148-d1ae-46d6-bff4-6dffb75aa0e5' class='xr-var-data-in' type='checkbox'><label for='data-db12c148-d1ae-46d6-bff4-6dffb75aa0e5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_configuration_names</span></div><div class='xr-var-dims'>(time, dim_5)</div><div class='xr-var-dtype'>&lt;U29</div><div class='xr-var-preview xr-preview'>&#x27;pe1_proc_configuration_names&#x27; ....</div><input id='attrs-3a8348c4-e7f4-4fa5-bd77-dbc671f67a5f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-3a8348c4-e7f4-4fa5-bd77-dbc671f67a5f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fd6383fb-2cb1-44b9-8177-3475163afd02' class='xr-var-data-in' type='checkbox'><label for='data-fd6383fb-2cb1-44b9-8177-3475163afd02' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_proc_configuration_names&#x27;, &#x27;pe1_proc_port_name&#x27;,
            &#x27;pe1_proc_asyn_pipeline_config&#x27;, &#x27;pe1_proc_blocking_callbacks&#x27;,
            &#x27;pe1_proc_data_type&#x27;, &#x27;pe1_proc_enable&#x27;,
            &#x27;pe1_proc_nd_array_port&#x27;, &#x27;pe1_proc_plugin_type&#x27;,
            &#x27;pe1_proc_auto_offset_scale&#x27;, &#x27;pe1_proc_auto_reset_filter&#x27;,
            &#x27;pe1_proc_copy_to_filter_seq&#x27;, &#x27;pe1_proc_data_type_out&#x27;,
            &#x27;pe1_proc_difference_seq&#x27;, &#x27;pe1_proc_enable_background&#x27;,
            &#x27;pe1_proc_enable_filter&#x27;, &#x27;pe1_proc_enable_flat_field&#x27;,
            &#x27;pe1_proc_enable_high_clip&#x27;, &#x27;pe1_proc_enable_low_clip&#x27;,
            &#x27;pe1_proc_enable_offset_scale&#x27;, &#x27;pe1_proc_fc&#x27;,
            &#x27;pe1_proc_foffset&#x27;, &#x27;pe1_proc_fscale&#x27;,
            &#x27;pe1_proc_filter_callbacks&#x27;, &#x27;pe1_proc_filter_type&#x27;,
            &#x27;pe1_proc_filter_type_seq&#x27;, &#x27;pe1_proc_high_clip&#x27;,
            &#x27;pe1_proc_low_clip&#x27;, &#x27;pe1_proc_num_filter&#x27;,
            &#x27;pe1_proc_num_filter_recip&#x27;, &#x27;pe1_proc_num_filtered&#x27;,
            &#x27;pe1_proc_oc&#x27;, &#x27;pe1_proc_o_offset&#x27;, &#x27;pe1_proc_o_scale&#x27;,
            &#x27;pe1_proc_offset&#x27;, &#x27;pe1_proc_rc&#x27;, &#x27;pe1_proc_roffset&#x27;,
            &#x27;pe1_proc_scale&#x27;, &#x27;pe1_proc_scale_flat_field&#x27;,
            &#x27;pe1_proc_valid_background&#x27;, &#x27;pe1_proc_valid_flat_field&#x27;]],
          dtype=&#x27;&lt;U29&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U5</div><div class='xr-var-preview xr-preview'>&#x27;PROC1&#x27;</div><input id='attrs-ea7da62e-8a39-464b-939e-5ef04c9bfdbf' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ea7da62e-8a39-464b-939e-5ef04c9bfdbf' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7470cbe1-e142-440c-835b-fa375b02a84d' class='xr-var-data-in' type='checkbox'><label for='data-7470cbe1-e142-440c-835b-fa375b02a84d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PROC1&#x27;], dtype=&#x27;&lt;U5&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_6)</div><div class='xr-var-dtype'>&lt;U28</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; &#x27;p...</div><input id='attrs-10a288dd-8301-4f8c-97d8-45560511f987' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-10a288dd-8301-4f8c-97d8-45560511f987' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-745b61b0-a2eb-4f5a-9220-6cea5a3478ba' class='xr-var-data-in' type='checkbox'><label for='data-745b61b0-a2eb-4f5a-9220-6cea5a3478ba' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_proc_configuration_names&#x27;]],
          dtype=&#x27;&lt;U28&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-9f122a69-6e1d-48db-8b7c-8b64441a90fc' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9f122a69-6e1d-48db-8b7c-8b64441a90fc' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d435bf4b-8c65-4268-9345-250e8b71b768' class='xr-var-data-in' type='checkbox'><label for='data-d435bf4b-8c65-4268-9345-250e8b71b768' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_data_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;UInt16&#x27;</div><input id='attrs-a0777b99-9289-44a7-a8ba-b797320920c4' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a0777b99-9289-44a7-a8ba-b797320920c4' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b5545739-8076-4bfd-a878-c742bce6ab2a' class='xr-var-data-in' type='checkbox'><label for='data-b5545739-8076-4bfd-a878-c742bce6ab2a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;UInt16&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-6bfd5bf0-984c-4a38-8850-bc699e2f2153' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6bfd5bf0-984c-4a38-8850-bc699e2f2153' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a26599db-ab0d-418c-b2f2-df77ddbd9083' class='xr-var-data-in' type='checkbox'><label for='data-a26599db-ab0d-418c-b2f2-df77ddbd9083' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;PEDET1&#x27;</div><input id='attrs-f5f43f07-ecd3-4b88-be76-396e42cc475b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f5f43f07-ecd3-4b88-be76-396e42cc475b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e2f2d921-6ea7-44f5-ba4b-c717a5f50d40' class='xr-var-data-in' type='checkbox'><label for='data-e2f2d921-6ea7-44f5-ba4b-c717a5f50d40' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PEDET1&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U15</div><div class='xr-var-preview xr-preview'>&#x27;NDPluginProcess&#x27;</div><input id='attrs-adf6671a-715b-48fa-bd13-3481aaf8e1d8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-adf6671a-715b-48fa-bd13-3481aaf8e1d8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b8f2e969-6d96-4d78-bab4-487d166bddf4' class='xr-var-data-in' type='checkbox'><label for='data-b8f2e969-6d96-4d78-bab4-487d166bddf4' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDPluginProcess&#x27;], dtype=&#x27;&lt;U15&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_auto_offset_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U4</div><div class='xr-var-preview xr-preview'>&#x27;Done&#x27;</div><input id='attrs-a0f88025-3b5d-44a7-b546-32f6e89eea92' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a0f88025-3b5d-44a7-b546-32f6e89eea92' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f711bdb3-6109-42c6-bf3a-4912796fcd96' class='xr-var-data-in' type='checkbox'><label for='data-f711bdb3-6109-42c6-bf3a-4912796fcd96' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Done&#x27;], dtype=&#x27;&lt;U4&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_auto_reset_filter</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-995f473a-39ec-4c1b-a3d2-4076a7aeeac9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-995f473a-39ec-4c1b-a3d2-4076a7aeeac9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-985cb840-1baa-45ba-a155-0bd737e8f3bb' class='xr-var-data-in' type='checkbox'><label for='data-985cb840-1baa-45ba-a155-0bd737e8f3bb' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_copy_to_filter_seq</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-08766ad2-437d-40a2-afa2-876d53568650' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-08766ad2-437d-40a2-afa2-876d53568650' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f8513498-d737-4e55-836b-c7aff70e1f00' class='xr-var-data-in' type='checkbox'><label for='data-f8513498-d737-4e55-836b-c7aff70e1f00' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_data_type_out</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>&#x27;Automatic&#x27;</div><input id='attrs-e7f3fac0-9ce6-413f-b2e1-c2de404eac72' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e7f3fac0-9ce6-413f-b2e1-c2de404eac72' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ad301ee4-da10-4e6f-bd07-8093d21da9fa' class='xr-var-data-in' type='checkbox'><label for='data-ad301ee4-da10-4e6f-bd07-8093d21da9fa' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Automatic&#x27;], dtype=&#x27;&lt;U9&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_difference_seq</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-21ecbd62-6a4e-4733-9151-cd14df53185b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-21ecbd62-6a4e-4733-9151-cd14df53185b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c0b67729-18c0-4a8a-bc51-8f5517888fca' class='xr-var-data-in' type='checkbox'><label for='data-c0b67729-18c0-4a8a-bc51-8f5517888fca' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_background</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-0642cc8e-b0b0-4f4c-9057-6a987b102ff6' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0642cc8e-b0b0-4f4c-9057-6a987b102ff6' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5e20025e-bb4a-418c-b933-f2490d668ab2' class='xr-var-data-in' type='checkbox'><label for='data-5e20025e-bb4a-418c-b933-f2490d668ab2' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_filter</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-d0450e72-5562-41ee-83f3-418c75250b96' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-d0450e72-5562-41ee-83f3-418c75250b96' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7c45fdb7-ab62-4abe-9286-8093131fbdee' class='xr-var-data-in' type='checkbox'><label for='data-7c45fdb7-ab62-4abe-9286-8093131fbdee' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_flat_field</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-28cf18ea-cba7-4d94-a811-e26afa9fe54e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-28cf18ea-cba7-4d94-a811-e26afa9fe54e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2e82aa90-65d9-4f5f-b3f9-e80739919167' class='xr-var-data-in' type='checkbox'><label for='data-2e82aa90-65d9-4f5f-b3f9-e80739919167' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_high_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-0619bdbd-e1c0-4d05-a905-08ae4fd93f43' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0619bdbd-e1c0-4d05-a905-08ae4fd93f43' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2cba5e43-24f8-4a50-a586-b4265fe816fa' class='xr-var-data-in' type='checkbox'><label for='data-2cba5e43-24f8-4a50-a586-b4265fe816fa' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_low_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-beaae786-2133-4402-98be-01f6ac94a7e5' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-beaae786-2133-4402-98be-01f6ac94a7e5' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-569b0984-6443-4a8b-9084-19170fd30037' class='xr-var-data-in' type='checkbox'><label for='data-569b0984-6443-4a8b-9084-19170fd30037' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_offset_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-e6bd094a-2b7d-4f61-88be-3b3300908a6f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e6bd094a-2b7d-4f61-88be-3b3300908a6f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-cb4aac9a-4959-4213-beba-516f1f8e75c1' class='xr-var-data-in' type='checkbox'><label for='data-cb4aac9a-4959-4213-beba-516f1f8e75c1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_foffset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-13e6b3e2-0596-462d-b485-6bd5633bd403' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-13e6b3e2-0596-462d-b485-6bd5633bd403' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2f4b1952-51a8-4bed-ad31-076c6dc36666' class='xr-var-data-in' type='checkbox'><label for='data-2f4b1952-51a8-4bed-ad31-076c6dc36666' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_fscale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-38688ef6-65d2-4a02-a4d3-90f5871c6956' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-38688ef6-65d2-4a02-a4d3-90f5871c6956' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a895699b-6ef7-4090-8776-a7597dc534ff' class='xr-var-data-in' type='checkbox'><label for='data-a895699b-6ef7-4090-8776-a7597dc534ff' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_filter_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U12</div><div class='xr-var-preview xr-preview'>&#x27;Array N only&#x27;</div><input id='attrs-6f80383d-41ae-4ed7-9f82-2a8371530ca7' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6f80383d-41ae-4ed7-9f82-2a8371530ca7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-026bcd6f-e62c-4dc6-93ae-ae0b5201af49' class='xr-var-data-in' type='checkbox'><label for='data-026bcd6f-e62c-4dc6-93ae-ae0b5201af49' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Array N only&#x27;], dtype=&#x27;&lt;U12&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_filter_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Average&#x27;</div><input id='attrs-2755db20-ea8f-4ed8-a88d-712701a29092' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-2755db20-ea8f-4ed8-a88d-712701a29092' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6d2f88c1-c1fe-4e77-9024-0d1f63f3aaed' class='xr-var-data-in' type='checkbox'><label for='data-6d2f88c1-c1fe-4e77-9024-0d1f63f3aaed' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Average&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_filter_type_seq</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-de26b0f6-c4c0-4983-92c2-20c0ffd0622d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-de26b0f6-c4c0-4983-92c2-20c0ffd0622d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-cb57e02c-7fd7-4822-905b-38072342e8ef' class='xr-var-data-in' type='checkbox'><label for='data-cb57e02c-7fd7-4822-905b-38072342e8ef' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_high_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>100.0</div><input id='attrs-02494f3b-3d4a-47bc-83b3-b2ede45a44de' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-02494f3b-3d4a-47bc-83b3-b2ede45a44de' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fe914c75-b4c0-49c4-bc91-250c9e2ef9a1' class='xr-var-data-in' type='checkbox'><label for='data-fe914c75-b4c0-49c4-bc91-250c9e2ef9a1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([100.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_low_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-b1bc18ce-5563-46a1-8f1c-f27c7db48a37' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b1bc18ce-5563-46a1-8f1c-f27c7db48a37' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-986cf24b-9e3e-4ba1-a29f-c3e995f9513e' class='xr-var-data-in' type='checkbox'><label for='data-986cf24b-9e3e-4ba1-a29f-c3e995f9513e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_num_filter</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>50</div><input id='attrs-54747154-c678-4314-9f72-701885055adc' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-54747154-c678-4314-9f72-701885055adc' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3e13e927-3e73-4ce8-9cfa-217d6510da50' class='xr-var-data-in' type='checkbox'><label for='data-3e13e927-3e73-4ce8-9cfa-217d6510da50' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([50])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_num_filter_recip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.02</div><input id='attrs-19261d90-98fb-45b3-9da3-c488167c75d0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-19261d90-98fb-45b3-9da3-c488167c75d0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c53a4fa3-06b4-47b8-87ee-d9407137a455' class='xr-var-data-in' type='checkbox'><label for='data-c53a4fa3-06b4-47b8-87ee-d9407137a455' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.02])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_num_filtered</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>2</div><input id='attrs-6e8515c3-3e68-4e4f-aa8c-de5d5d5b143e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6e8515c3-3e68-4e4f-aa8c-de5d5d5b143e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b5fea3cf-0ab6-4ee0-a09e-97e1fb3a999b' class='xr-var-data-in' type='checkbox'><label for='data-b5fea3cf-0ab6-4ee0-a09e-97e1fb3a999b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([2])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_o_offset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-92a45a85-580f-4ef8-861d-3442312f83d0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-92a45a85-580f-4ef8-861d-3442312f83d0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c7a1ac41-393b-4726-8719-2ac6c13f70ed' class='xr-var-data-in' type='checkbox'><label for='data-c7a1ac41-393b-4726-8719-2ac6c13f70ed' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_o_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-1be49d3e-0bfa-40eb-8de5-6c4e844ae3ca' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-1be49d3e-0bfa-40eb-8de5-6c4e844ae3ca' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2594ed7f-8190-4f64-b75e-940ec260ff2a' class='xr-var-data-in' type='checkbox'><label for='data-2594ed7f-8190-4f64-b75e-940ec260ff2a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_offset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-4a7485e1-7031-440a-90ea-2ae603d7ebc5' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4a7485e1-7031-440a-90ea-2ae603d7ebc5' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-999f8708-382b-445a-b602-dcd83147bf95' class='xr-var-data-in' type='checkbox'><label for='data-999f8708-382b-445a-b602-dcd83147bf95' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_roffset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-34274614-664c-4528-8144-8b17da92dbc1' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-34274614-664c-4528-8144-8b17da92dbc1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2ba582ca-f8a8-44d8-bacb-74311b9fe39e' class='xr-var-data-in' type='checkbox'><label for='data-2ba582ca-f8a8-44d8-bacb-74311b9fe39e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-5d77926d-0cbe-44db-ad62-338ba12231a9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5d77926d-0cbe-44db-ad62-338ba12231a9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-50f01941-68ec-4942-9be8-791d42f91894' class='xr-var-data-in' type='checkbox'><label for='data-50f01941-68ec-4942-9be8-791d42f91894' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_scale_flat_field</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>255.0</div><input id='attrs-83b5e1a0-cf4d-473a-8329-7ed68704791a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-83b5e1a0-cf4d-473a-8329-7ed68704791a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7588f235-9697-4f2c-9ef1-a01db465f5c5' class='xr-var-data-in' type='checkbox'><label for='data-7588f235-9697-4f2c-9ef1-a01db465f5c5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([255.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_valid_background</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Invalid&#x27;</div><input id='attrs-87c7660f-fad0-4601-97f6-edd0d7018885' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-87c7660f-fad0-4601-97f6-edd0d7018885' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7f9055d4-df10-4a61-aaad-c4bb963b4aab' class='xr-var-data-in' type='checkbox'><label for='data-7f9055d4-df10-4a61-aaad-c4bb963b4aab' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Invalid&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_valid_flat_field</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Invalid&#x27;</div><input id='attrs-4a76f031-d11f-41cd-b013-c810d8930a01' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4a76f031-d11f-41cd-b013-c810d8930a01' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7fdf7599-5aab-49a8-a7a6-ece8e808c7d2' class='xr-var-data-in' type='checkbox'><label for='data-7fdf7599-5aab-49a8-a7a6-ece8e808c7d2' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Invalid&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_images_per_set</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>50.0</div><input id='attrs-6ac9db28-56a4-4a6a-a93d-e3a1288903cb' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6ac9db28-56a4-4a6a-a93d-e3a1288903cb' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c6edd3dd-0400-47f4-b92f-62cbd1dff31a' class='xr-var-data-in' type='checkbox'><label for='data-c6edd3dd-0400-47f4-b92f-62cbd1dff31a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([50.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_number_of_sets</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-dcdad4ff-adef-499d-b5cc-766f9d2a7748' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-dcdad4ff-adef-499d-b5cc-766f9d2a7748' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4bb7c119-c812-4948-8e0c-08afb7d334b7' class='xr-var-data-in' type='checkbox'><label for='data-4bb7c119-c812-4948-8e0c-08afb7d334b7' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_pixel_size</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0002</div><input id='attrs-9a4e0ce1-1d3a-430d-bbd0-dc4c9e823939' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9a4e0ce1-1d3a-430d-bbd0-dc4c9e823939' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-646a2e11-1c72-4d68-b9e2-cef11b451351' class='xr-var-data-in' type='checkbox'><label for='data-646a2e11-1c72-4d68-b9e2-cef11b451351' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.0002])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_detector_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Perkin&#x27;</div><input id='attrs-b10acf9b-4c66-4a09-8b03-a8593f9965d0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b10acf9b-4c66-4a09-8b03-a8593f9965d0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-eafa809d-afee-49f8-8c5e-f50345f7fd40' class='xr-var-data-in' type='checkbox'><label for='data-eafa809d-afee-49f8-8c5e-f50345f7fd40' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Perkin&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_configuration_names</span></div><div class='xr-var-dims'>(time, dim_7)</div><div class='xr-var-dtype'>&lt;U31</div><div class='xr-var-preview xr-preview'>&#x27;pe1_stats1_configuration_names&#x27;...</div><input id='attrs-36841728-ac88-42cc-9538-6df9ba3c626a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-36841728-ac88-42cc-9538-6df9ba3c626a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-648ca674-fe56-4182-a9ea-b288039e2e30' class='xr-var-data-in' type='checkbox'><label for='data-648ca674-fe56-4182-a9ea-b288039e2e30' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_stats1_configuration_names&#x27;, &#x27;pe1_stats1_port_name&#x27;,
            &#x27;pe1_stats1_asyn_pipeline_config&#x27;,
            &#x27;pe1_stats1_blocking_callbacks&#x27;, &#x27;pe1_stats1_enable&#x27;,
            &#x27;pe1_stats1_nd_array_port&#x27;, &#x27;pe1_stats1_plugin_type&#x27;,
            &#x27;pe1_stats1_bgd_width&#x27;, &#x27;pe1_stats1_centroid_threshold&#x27;,
            &#x27;pe1_stats1_compute_centroid&#x27;, &#x27;pe1_stats1_compute_histogram&#x27;,
            &#x27;pe1_stats1_compute_profiles&#x27;, &#x27;pe1_stats1_compute_statistics&#x27;,
            &#x27;pe1_stats1_hist_max&#x27;, &#x27;pe1_stats1_hist_min&#x27;,
            &#x27;pe1_stats1_hist_size&#x27;, &#x27;pe1_stats1_profile_cursor&#x27;,
            &#x27;pe1_stats1_profile_size&#x27;, &#x27;pe1_stats1_ts_num_points&#x27;]],
          dtype=&#x27;&lt;U31&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;STATS1&#x27;</div><input id='attrs-99eaed48-9203-402f-b978-31ca79f0ecca' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-99eaed48-9203-402f-b978-31ca79f0ecca' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fece505a-a020-4d0a-ba21-cf6ed9837a5a' class='xr-var-data-in' type='checkbox'><label for='data-fece505a-a020-4d0a-ba21-cf6ed9837a5a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;STATS1&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_8)</div><div class='xr-var-dtype'>&lt;U30</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; .....</div><input id='attrs-030df49c-4a7a-4f1f-bb01-5954bcfeb1e4' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-030df49c-4a7a-4f1f-bb01-5954bcfeb1e4' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5b24bd6a-ecb1-44ae-855d-82f0b4a70093' class='xr-var-data-in' type='checkbox'><label for='data-5b24bd6a-ecb1-44ae-855d-82f0b4a70093' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_roi1_configuration_names&#x27;,
            &#x27;pe1_stats1_configuration_names&#x27;]], dtype=&#x27;&lt;U30&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-a4d979d2-7ae0-41aa-8695-19999f8d1447' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a4d979d2-7ae0-41aa-8695-19999f8d1447' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6abdda96-efbb-40a0-a7fc-51d6038226dc' class='xr-var-data-in' type='checkbox'><label for='data-6abdda96-efbb-40a0-a7fc-51d6038226dc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-dc9ea8ae-51ef-46f5-9a18-abefa716b3ca' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-dc9ea8ae-51ef-46f5-9a18-abefa716b3ca' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-837f82d4-7570-4ae3-a696-3c25a1d1de80' class='xr-var-data-in' type='checkbox'><label for='data-837f82d4-7570-4ae3-a696-3c25a1d1de80' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U4</div><div class='xr-var-preview xr-preview'>&#x27;ROI1&#x27;</div><input id='attrs-e425ad39-557e-42ce-b7e6-6b7244e999d0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e425ad39-557e-42ce-b7e6-6b7244e999d0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9a80bfb0-640f-4913-9cca-485366e828a1' class='xr-var-data-in' type='checkbox'><label for='data-9a80bfb0-640f-4913-9cca-485366e828a1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;ROI1&#x27;], dtype=&#x27;&lt;U4&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U13</div><div class='xr-var-preview xr-preview'>&#x27;NDPluginStats&#x27;</div><input id='attrs-6520e82c-90ac-4bc8-a9e2-2095e96bdd3f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6520e82c-90ac-4bc8-a9e2-2095e96bdd3f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-bfdcef93-c524-4402-9e1e-cf28633a6772' class='xr-var-data-in' type='checkbox'><label for='data-bfdcef93-c524-4402-9e1e-cf28633a6772' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDPluginStats&#x27;], dtype=&#x27;&lt;U13&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_bgd_width</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-fe024d7d-ae18-439f-b5bf-dcd6551d4ff5' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-fe024d7d-ae18-439f-b5bf-dcd6551d4ff5' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-eb242177-5776-46df-9e1f-885a9db2e560' class='xr-var-data-in' type='checkbox'><label for='data-eb242177-5776-46df-9e1f-885a9db2e560' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_centroid_threshold</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-0f86986b-99df-4a56-a008-95ac78a809c7' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0f86986b-99df-4a56-a008-95ac78a809c7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-118dcf83-8e2c-441d-9e0d-5fc4cfbc3804' class='xr-var-data-in' type='checkbox'><label for='data-118dcf83-8e2c-441d-9e0d-5fc4cfbc3804' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_centroid</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U2</div><div class='xr-var-preview xr-preview'>&#x27;No&#x27;</div><input id='attrs-2d0b1491-4141-4393-ba0f-b898cc1349c5' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-2d0b1491-4141-4393-ba0f-b898cc1349c5' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5fc7945d-5507-448c-888e-366c3a1c54fc' class='xr-var-data-in' type='checkbox'><label for='data-5fc7945d-5507-448c-888e-366c3a1c54fc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;No&#x27;], dtype=&#x27;&lt;U2&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_histogram</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U2</div><div class='xr-var-preview xr-preview'>&#x27;No&#x27;</div><input id='attrs-da1b67d1-96d3-4eef-91df-2c68db2a583e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-da1b67d1-96d3-4eef-91df-2c68db2a583e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5ad0d3f8-c1a3-4c9f-8274-861efde7606c' class='xr-var-data-in' type='checkbox'><label for='data-5ad0d3f8-c1a3-4c9f-8274-861efde7606c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;No&#x27;], dtype=&#x27;&lt;U2&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_profiles</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U2</div><div class='xr-var-preview xr-preview'>&#x27;No&#x27;</div><input id='attrs-c52a6d73-59a5-40ab-b6f3-7345b74c0953' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c52a6d73-59a5-40ab-b6f3-7345b74c0953' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-045dbde8-110f-4906-97be-8518b66b02c0' class='xr-var-data-in' type='checkbox'><label for='data-045dbde8-110f-4906-97be-8518b66b02c0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;No&#x27;], dtype=&#x27;&lt;U2&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_statistics</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-44f4b572-ad08-4a62-b05b-53d6f484bbcd' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-44f4b572-ad08-4a62-b05b-53d6f484bbcd' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5f8ec45f-361c-4b69-8455-399c5a21c1c2' class='xr-var-data-in' type='checkbox'><label for='data-5f8ec45f-361c-4b69-8455-399c5a21c1c2' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_hist_max</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>255.0</div><input id='attrs-c5cc0f8f-b61c-4f69-8f00-0dfca9b8ffc2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c5cc0f8f-b61c-4f69-8f00-0dfca9b8ffc2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a00b3772-1707-4c95-b10c-1d7692c6e534' class='xr-var-data-in' type='checkbox'><label for='data-a00b3772-1707-4c95-b10c-1d7692c6e534' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([255.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_hist_min</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-96d6ef6c-960c-4fc2-b9c1-6a719b32eb13' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-96d6ef6c-960c-4fc2-b9c1-6a719b32eb13' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3a9b7776-6e4e-479a-a059-1f82ec84639f' class='xr-var-data-in' type='checkbox'><label for='data-3a9b7776-6e4e-479a-a059-1f82ec84639f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_hist_size</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>256</div><input id='attrs-8e84329d-94ef-4a3c-b6aa-9ce97925a004' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8e84329d-94ef-4a3c-b6aa-9ce97925a004' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7cce253c-e88b-430d-b726-4222513d160d' class='xr-var-data-in' type='checkbox'><label for='data-7cce253c-e88b-430d-b726-4222513d160d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([256])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_ts_num_points</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>2048</div><input id='attrs-acf00a30-501e-4638-b3be-60cd74b7df10' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-acf00a30-501e-4638-b3be-60cd74b7df10' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-84fba8a8-20ab-44bc-8347-43fc6479f56a' class='xr-var-data-in' type='checkbox'><label for='data-84fba8a8-20ab-44bc-8347-43fc6479f56a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([2048])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_configuration_names</span></div><div class='xr-var-dims'>(time, dim_9)</div><div class='xr-var-dtype'>&lt;U29</div><div class='xr-var-preview xr-preview'>&#x27;pe1_roi1_configuration_names&#x27; ....</div><input id='attrs-0aada1f0-9306-41b1-b863-c8298914a070' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0aada1f0-9306-41b1-b863-c8298914a070' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-dec232ea-418e-4a82-808a-e4d4e1d82de9' class='xr-var-data-in' type='checkbox'><label for='data-dec232ea-418e-4a82-808a-e4d4e1d82de9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_roi1_configuration_names&#x27;, &#x27;pe1_roi1_port_name&#x27;,
            &#x27;pe1_roi1_asyn_pipeline_config&#x27;, &#x27;pe1_roi1_blocking_callbacks&#x27;,
            &#x27;pe1_roi1_enable&#x27;, &#x27;pe1_roi1_nd_array_port&#x27;,
            &#x27;pe1_roi1_plugin_type&#x27;, &#x27;pe1_roi1_bin_&#x27;,
            &#x27;pe1_roi1_data_type_out&#x27;, &#x27;pe1_roi1_enable_scale&#x27;,
            &#x27;pe1_roi1_roi_enable&#x27;, &#x27;pe1_roi1_min_xyz&#x27;, &#x27;pe1_roi1_name_&#x27;,
            &#x27;pe1_roi1_size&#x27;]], dtype=&#x27;&lt;U29&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U4</div><div class='xr-var-preview xr-preview'>&#x27;ROI1&#x27;</div><input id='attrs-10a07cc8-8d6e-4de2-9c23-d1bb0cc496d1' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-10a07cc8-8d6e-4de2-9c23-d1bb0cc496d1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-bf8d93fa-2b4e-4ee1-9931-9acd557771a5' class='xr-var-data-in' type='checkbox'><label for='data-bf8d93fa-2b4e-4ee1-9931-9acd557771a5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;ROI1&#x27;], dtype=&#x27;&lt;U4&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_10)</div><div class='xr-var-dtype'>&lt;U28</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; &#x27;p...</div><input id='attrs-3df33516-4f51-4fc0-9698-5021ad6ea7fc' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-3df33516-4f51-4fc0-9698-5021ad6ea7fc' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-340ae195-310c-4d95-8065-1b304fd0ca43' class='xr-var-data-in' type='checkbox'><label for='data-340ae195-310c-4d95-8065-1b304fd0ca43' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_roi1_configuration_names&#x27;]],
          dtype=&#x27;&lt;U28&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-f2b0783b-4f89-4997-89a1-8ae73250be5d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f2b0783b-4f89-4997-89a1-8ae73250be5d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-84dd5c46-4d09-40ef-80b8-f5e7d632a909' class='xr-var-data-in' type='checkbox'><label for='data-84dd5c46-4d09-40ef-80b8-f5e7d632a909' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-e07cf51c-32de-4bb3-9710-d34c56880f24' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e07cf51c-32de-4bb3-9710-d34c56880f24' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7753ced6-8f18-4163-a6c3-5484991aa2de' class='xr-var-data-in' type='checkbox'><label for='data-7753ced6-8f18-4163-a6c3-5484991aa2de' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;PEDET1&#x27;</div><input id='attrs-e07eca6e-eb8f-4ec3-8d69-cd39522246ef' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e07eca6e-eb8f-4ec3-8d69-cd39522246ef' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a6a05be0-d516-4cef-99e8-fe72563d150d' class='xr-var-data-in' type='checkbox'><label for='data-a6a05be0-d516-4cef-99e8-fe72563d150d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PEDET1&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U11</div><div class='xr-var-preview xr-preview'>&#x27;NDPluginROI&#x27;</div><input id='attrs-986d53f0-f5f9-4e3b-a252-cf65f01e4f43' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-986d53f0-f5f9-4e3b-a252-cf65f01e4f43' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-29300aea-5cef-4e77-b458-ab92f3bc4334' class='xr-var-data-in' type='checkbox'><label for='data-29300aea-5cef-4e77-b458-ab92f3bc4334' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDPluginROI&#x27;], dtype=&#x27;&lt;U11&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_data_type_out</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>&#x27;Automatic&#x27;</div><input id='attrs-7e6d48d3-dfe4-451c-b028-dc6695efd1d6' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7e6d48d3-dfe4-451c-b028-dc6695efd1d6' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9e5095dd-5a4a-4c4a-9584-944429d5aae1' class='xr-var-data-in' type='checkbox'><label for='data-9e5095dd-5a4a-4c4a-9584-944429d5aae1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Automatic&#x27;], dtype=&#x27;&lt;U9&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_enable_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-f8c11e9f-599c-4240-9734-9efba8ea4090' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f8c11e9f-599c-4240-9734-9efba8ea4090' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-98605f5b-837b-4b34-83c2-8d02d451ff49' class='xr-var-data-in' type='checkbox'><label for='data-98605f5b-837b-4b34-83c2-8d02d451ff49' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_name_</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U1</div><div class='xr-var-preview xr-preview'>&#x27;&#x27;</div><input id='attrs-af8373ac-a84c-4542-a825-7db1ebdd434c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-af8373ac-a84c-4542-a825-7db1ebdd434c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a9de3a49-7a3f-4618-bc72-1d3f32b9be33' class='xr-var-data-in' type='checkbox'><label for='data-a9de3a49-7a3f-4618-bc72-1d3f32b9be33' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;&#x27;], dtype=&#x27;&lt;U1&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>seq_num</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-9a04cfe2-3ee1-424c-8e41-5f11db716147' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9a04cfe2-3ee1-424c-8e41-5f11db716147' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-076890e3-59a7-44d5-ae22-156a83169ed8' class='xr-var-data-in' type='checkbox'><label for='data-076890e3-59a7-44d5-ae22-156a83169ed8' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>uid</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U36</div><div class='xr-var-preview xr-preview'>&#x27;ad3b7a7f-6564-4157-933f-c3bae9e...</div><input id='attrs-98780590-bd1e-4f9a-9c7c-66e275fbc1be' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-98780590-bd1e-4f9a-9c7c-66e275fbc1be' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9b9a64d8-76cf-4f00-97bf-0f91e49aee2c' class='xr-var-data-in' type='checkbox'><label for='data-9b9a64d8-76cf-4f00-97bf-0f91e49aee2c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;ad3b7a7f-6564-4157-933f-c3bae9e9e876&#x27;], dtype=&#x27;&lt;U36&#x27;)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-9df5647b-e3dc-40df-90a8-f7be11c78824' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-9df5647b-e3dc-40df-90a8-f7be11c78824' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>
    <br />
    <br />

The data is processed by the analyzer is the diffraction image.


.. code-block:: default


    raw_data["pe1_image"][0].plot()




.. image:: /tutorials2/images/sphx_glr_plot_xpd_analyzer_001.png
    :alt: time = 1581814176.5086372
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    <matplotlib.collections.QuadMesh object at 0x7fa4e0801c10>



In both ways, we need to use string values even if the ``qmax`` is actually a number.

After we run either line of the code above, the analyzer will use ``qmax = 20`` in the data processing.

Process the data
^^^^^^^^^^^^^^^^

We use the analyzer to process the data.


.. code-block:: default


    analyzer.analyze(run)








Get processed data from databroker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The data is dumped into databroker ``an_db`` by the analyzer.
We retrieve the last run in the database and it should be the processed data from our analyzer.


.. code-block:: default


    an_db = config.an_db
    an_run = an_db[-1]








Here, we show the processed data in an xarray.


.. code-block:: default


    an_data = an_run.primary.read()
    an_data






.. raw:: html

    <div><svg style="position: absolute; width: 0; height: 0; overflow: hidden">
    <defs>
    <symbol id="icon-database" viewBox="0 0 32 32">
    <path d="M16 0c-8.837 0-16 2.239-16 5v4c0 2.761 7.163 5 16 5s16-2.239 16-5v-4c0-2.761-7.163-5-16-5z"></path>
    <path d="M16 17c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
    <path d="M16 26c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
    </symbol>
    <symbol id="icon-file-text2" viewBox="0 0 32 32">
    <path d="M28.681 7.159c-0.694-0.947-1.662-2.053-2.724-3.116s-2.169-2.030-3.116-2.724c-1.612-1.182-2.393-1.319-2.841-1.319h-15.5c-1.378 0-2.5 1.121-2.5 2.5v27c0 1.378 1.122 2.5 2.5 2.5h23c1.378 0 2.5-1.122 2.5-2.5v-19.5c0-0.448-0.137-1.23-1.319-2.841zM24.543 5.457c0.959 0.959 1.712 1.825 2.268 2.543h-4.811v-4.811c0.718 0.556 1.584 1.309 2.543 2.268zM28 29.5c0 0.271-0.229 0.5-0.5 0.5h-23c-0.271 0-0.5-0.229-0.5-0.5v-27c0-0.271 0.229-0.5 0.5-0.5 0 0 15.499-0 15.5 0v7c0 0.552 0.448 1 1 1h7v19.5z"></path>
    <path d="M23 26h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    <path d="M23 22h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    <path d="M23 18h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    </symbol>
    </defs>
    </svg>
    <style>/* CSS stylesheet for displaying xarray objects in jupyterlab.
     *
     */

    :root {
      --xr-font-color0: var(--jp-content-font-color0, rgba(0, 0, 0, 1));
      --xr-font-color2: var(--jp-content-font-color2, rgba(0, 0, 0, 0.54));
      --xr-font-color3: var(--jp-content-font-color3, rgba(0, 0, 0, 0.38));
      --xr-border-color: var(--jp-border-color2, #e0e0e0);
      --xr-disabled-color: var(--jp-layout-color3, #bdbdbd);
      --xr-background-color: var(--jp-layout-color0, white);
      --xr-background-color-row-even: var(--jp-layout-color1, white);
      --xr-background-color-row-odd: var(--jp-layout-color2, #eeeeee);
    }

    html[theme=dark],
    body.vscode-dark {
      --xr-font-color0: rgba(255, 255, 255, 1);
      --xr-font-color2: rgba(255, 255, 255, 0.54);
      --xr-font-color3: rgba(255, 255, 255, 0.38);
      --xr-border-color: #1F1F1F;
      --xr-disabled-color: #515151;
      --xr-background-color: #111111;
      --xr-background-color-row-even: #111111;
      --xr-background-color-row-odd: #313131;
    }

    .xr-wrap {
      display: block;
      min-width: 300px;
      max-width: 700px;
    }

    .xr-text-repr-fallback {
      /* fallback to plain text repr when CSS is not injected (untrusted notebook) */
      display: none;
    }

    .xr-header {
      padding-top: 6px;
      padding-bottom: 6px;
      margin-bottom: 4px;
      border-bottom: solid 1px var(--xr-border-color);
    }

    .xr-header > div,
    .xr-header > ul {
      display: inline;
      margin-top: 0;
      margin-bottom: 0;
    }

    .xr-obj-type,
    .xr-array-name {
      margin-left: 2px;
      margin-right: 10px;
    }

    .xr-obj-type {
      color: var(--xr-font-color2);
    }

    .xr-sections {
      padding-left: 0 !important;
      display: grid;
      grid-template-columns: 150px auto auto 1fr 20px 20px;
    }

    .xr-section-item {
      display: contents;
    }

    .xr-section-item input {
      display: none;
    }

    .xr-section-item input + label {
      color: var(--xr-disabled-color);
    }

    .xr-section-item input:enabled + label {
      cursor: pointer;
      color: var(--xr-font-color2);
    }

    .xr-section-item input:enabled + label:hover {
      color: var(--xr-font-color0);
    }

    .xr-section-summary {
      grid-column: 1;
      color: var(--xr-font-color2);
      font-weight: 500;
    }

    .xr-section-summary > span {
      display: inline-block;
      padding-left: 0.5em;
    }

    .xr-section-summary-in:disabled + label {
      color: var(--xr-font-color2);
    }

    .xr-section-summary-in + label:before {
      display: inline-block;
      content: '►';
      font-size: 11px;
      width: 15px;
      text-align: center;
    }

    .xr-section-summary-in:disabled + label:before {
      color: var(--xr-disabled-color);
    }

    .xr-section-summary-in:checked + label:before {
      content: '▼';
    }

    .xr-section-summary-in:checked + label > span {
      display: none;
    }

    .xr-section-summary,
    .xr-section-inline-details {
      padding-top: 4px;
      padding-bottom: 4px;
    }

    .xr-section-inline-details {
      grid-column: 2 / -1;
    }

    .xr-section-details {
      display: none;
      grid-column: 1 / -1;
      margin-bottom: 5px;
    }

    .xr-section-summary-in:checked ~ .xr-section-details {
      display: contents;
    }

    .xr-array-wrap {
      grid-column: 1 / -1;
      display: grid;
      grid-template-columns: 20px auto;
    }

    .xr-array-wrap > label {
      grid-column: 1;
      vertical-align: top;
    }

    .xr-preview {
      color: var(--xr-font-color3);
    }

    .xr-array-preview,
    .xr-array-data {
      padding: 0 5px !important;
      grid-column: 2;
    }

    .xr-array-data,
    .xr-array-in:checked ~ .xr-array-preview {
      display: none;
    }

    .xr-array-in:checked ~ .xr-array-data,
    .xr-array-preview {
      display: inline-block;
    }

    .xr-dim-list {
      display: inline-block !important;
      list-style: none;
      padding: 0 !important;
      margin: 0;
    }

    .xr-dim-list li {
      display: inline-block;
      padding: 0;
      margin: 0;
    }

    .xr-dim-list:before {
      content: '(';
    }

    .xr-dim-list:after {
      content: ')';
    }

    .xr-dim-list li:not(:last-child):after {
      content: ',';
      padding-right: 5px;
    }

    .xr-has-index {
      font-weight: bold;
    }

    .xr-var-list,
    .xr-var-item {
      display: contents;
    }

    .xr-var-item > div,
    .xr-var-item label,
    .xr-var-item > .xr-var-name span {
      background-color: var(--xr-background-color-row-even);
      margin-bottom: 0;
    }

    .xr-var-item > .xr-var-name:hover span {
      padding-right: 5px;
    }

    .xr-var-list > li:nth-child(odd) > div,
    .xr-var-list > li:nth-child(odd) > label,
    .xr-var-list > li:nth-child(odd) > .xr-var-name span {
      background-color: var(--xr-background-color-row-odd);
    }

    .xr-var-name {
      grid-column: 1;
    }

    .xr-var-dims {
      grid-column: 2;
    }

    .xr-var-dtype {
      grid-column: 3;
      text-align: right;
      color: var(--xr-font-color2);
    }

    .xr-var-preview {
      grid-column: 4;
    }

    .xr-var-name,
    .xr-var-dims,
    .xr-var-dtype,
    .xr-preview,
    .xr-attrs dt {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      padding-right: 10px;
    }

    .xr-var-name:hover,
    .xr-var-dims:hover,
    .xr-var-dtype:hover,
    .xr-attrs dt:hover {
      overflow: visible;
      width: auto;
      z-index: 1;
    }

    .xr-var-attrs,
    .xr-var-data {
      display: none;
      background-color: var(--xr-background-color) !important;
      padding-bottom: 5px !important;
    }

    .xr-var-attrs-in:checked ~ .xr-var-attrs,
    .xr-var-data-in:checked ~ .xr-var-data {
      display: block;
    }

    .xr-var-data > table {
      float: right;
    }

    .xr-var-name span,
    .xr-var-data,
    .xr-attrs {
      padding-left: 25px !important;
    }

    .xr-attrs,
    .xr-var-attrs,
    .xr-var-data {
      grid-column: 1 / -1;
    }

    dl.xr-attrs {
      padding: 0;
      margin: 0;
      display: grid;
      grid-template-columns: 125px auto;
    }

    .xr-attrs dt, dd {
      padding: 0;
      margin: 0;
      float: left;
      padding-right: 10px;
      width: auto;
    }

    .xr-attrs dt {
      font-weight: normal;
      grid-column: 1;
    }

    .xr-attrs dt:hover span {
      display: inline-block;
      background: var(--xr-background-color);
      padding-right: 10px;
    }

    .xr-attrs dd {
      grid-column: 2;
      white-space: pre-wrap;
      word-break: break-all;
    }

    .xr-icon-database,
    .xr-icon-file-text2 {
      display: inline-block;
      vertical-align: middle;
      width: 1em;
      height: 1.5em !important;
      stroke-width: 0;
      stroke: currentColor;
      fill: currentColor;
    }
    </style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt;
    Dimensions:       (dim_0: 2048, dim_1: 2048, dim_10: 692, dim_11: 692, dim_12: 692, dim_13: 692, dim_14: 3001, dim_15: 3001, dim_2: 2048, dim_3: 2048, dim_4: 2048, dim_5: 2048, dim_6: 1024, dim_7: 1024, dim_8: 755, dim_9: 755, time: 1)
    Coordinates:
      * time          (time) float64 1.607e+09
    Dimensions without coordinates: dim_0, dim_1, dim_10, dim_11, dim_12, dim_13, dim_14, dim_15, dim_2, dim_3, dim_4, dim_5, dim_6, dim_7, dim_8, dim_9
    Data variables:
        dk_sub_image  (time, dim_0, dim_1) uint16 0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0
        bg_sub_image  (time, dim_2, dim_3) uint16 0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0
        mask          (time, dim_4, dim_5) int64 1 1 1 1 1 1 1 1 ... 1 1 1 1 1 1 1 1
        chi_Q         (time, dim_6) float64 0.0253 0.05714 0.08897 ... 32.56 32.59
        chi_I         (time, dim_7) float32 17.449076 15.25509 17.243057 ... 0.0 0.0
        chi_max       (time) float32 21331.768
        chi_argmax    (time) float64 3.081
        iq_Q          (time, dim_8) float64 0.0 0.03183 0.06366 ... 23.94 23.97 24.0
        iq_I          (time, dim_9) float64 17.45 17.0 15.66 ... 74.84 74.1 73.68
        sq_Q          (time, dim_10) float64 0.0 0.03183 0.06366 ... 21.96 21.99
        sq_S          (time, dim_11) float64 1.441 1.42 1.399 ... 1.019 1.014 0.9995
        fq_Q          (time, dim_12) float64 0.0 0.03183 0.06366 ... 21.96 21.99
        fq_F          (time, dim_13) float64 0.0 0.01336 0.0254 ... 0.3035 -0.01125
        gr_r          (time, dim_14) float64 0.0 0.01 0.02 0.03 ... 29.98 29.99 30.0
        gr_G          (time, dim_15) float64 0.0 0.003567 0.006975 ... 1.4 1.455
        gr_max        (time) float64 7.417
        gr_argmax     (time) float64 6.59
        seq_num       (time) int64 1
        uid           (time) &lt;U36 &#x27;714d3474-7f29-4ee0-bee3-fe5d2171daea&#x27;</pre><div class='xr-wrap' hidden><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-24c4ddf4-af3f-4010-a8c2-4df49a9958b5' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-24c4ddf4-af3f-4010-a8c2-4df49a9958b5' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span>dim_0</span>: 2048</li><li><span>dim_1</span>: 2048</li><li><span>dim_10</span>: 692</li><li><span>dim_11</span>: 692</li><li><span>dim_12</span>: 692</li><li><span>dim_13</span>: 692</li><li><span>dim_14</span>: 3001</li><li><span>dim_15</span>: 3001</li><li><span>dim_2</span>: 2048</li><li><span>dim_3</span>: 2048</li><li><span>dim_4</span>: 2048</li><li><span>dim_5</span>: 2048</li><li><span>dim_6</span>: 1024</li><li><span>dim_7</span>: 1024</li><li><span>dim_8</span>: 755</li><li><span>dim_9</span>: 755</li><li><span class='xr-has-index'>time</span>: 1</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-d797299f-fac5-40d4-9fc4-3522e5afe287' class='xr-section-summary-in' type='checkbox'  checked><label for='section-d797299f-fac5-40d4-9fc4-3522e5afe287' class='xr-section-summary' >Coordinates: <span>(1)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.607e+09</div><input id='attrs-20e94927-b1d6-4316-9a4d-4f15d4bb5e4c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-20e94927-b1d6-4316-9a4d-4f15d4bb5e4c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5bf5c1c8-f16b-41d6-9b85-322caa7faae3' class='xr-var-data-in' type='checkbox'><label for='data-5bf5c1c8-f16b-41d6-9b85-322caa7faae3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.60704e+09])</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-2b7e688e-9922-4bf2-a1a7-a25057130d4d' class='xr-section-summary-in' type='checkbox'  ><label for='section-2b7e688e-9922-4bf2-a1a7-a25057130d4d' class='xr-section-summary' >Data variables: <span>(19)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>dk_sub_image</span></div><div class='xr-var-dims'>(time, dim_0, dim_1)</div><div class='xr-var-dtype'>uint16</div><div class='xr-var-preview xr-preview'>0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0</div><input id='attrs-66d0c876-b825-43ea-b34a-3ce3dab8b04c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-66d0c876-b825-43ea-b34a-3ce3dab8b04c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a71ed1ab-654c-422c-8e15-20f84318538c' class='xr-var-data-in' type='checkbox'><label for='data-a71ed1ab-654c-422c-8e15-20f84318538c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[    0,     0,     0, ...,     0,     0,     0],
            [    9,     1,     6, ...,     6,     4, 65534],
            [    4,    11,     4, ...,     6,     5,     2],
            ...,
            [    6, 65529,     4, ...,     7,     3, 65533],
            [    3,     2, 65533, ...,     7, 65535,     0],
            [    0,     0,     0, ...,     0,     0,     0]]], dtype=uint16)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>bg_sub_image</span></div><div class='xr-var-dims'>(time, dim_2, dim_3)</div><div class='xr-var-dtype'>uint16</div><div class='xr-var-preview xr-preview'>0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0</div><input id='attrs-a0d127e3-e96b-4e3c-abe1-36b9823dbaae' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a0d127e3-e96b-4e3c-abe1-36b9823dbaae' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2b9b6d3f-65a9-4410-8666-d2288ef86d5f' class='xr-var-data-in' type='checkbox'><label for='data-2b9b6d3f-65a9-4410-8666-d2288ef86d5f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[    0,     0,     0, ...,     0,     0,     0],
            [    9,     1,     6, ...,     6,     4, 65534],
            [    4,    11,     4, ...,     6,     5,     2],
            ...,
            [    6, 65529,     4, ...,     7,     3, 65533],
            [    3,     2, 65533, ...,     7, 65535,     0],
            [    0,     0,     0, ...,     0,     0,     0]]], dtype=uint16)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>mask</span></div><div class='xr-var-dims'>(time, dim_4, dim_5)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1 1 1 1 1 1 1 1 ... 1 1 1 1 1 1 1 1</div><input id='attrs-9a7733c0-7e52-46a0-bccc-5d160be90a4c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9a7733c0-7e52-46a0-bccc-5d160be90a4c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2a7be52d-ea45-4c50-a87d-265034537207' class='xr-var-data-in' type='checkbox'><label for='data-2a7be52d-ea45-4c50-a87d-265034537207' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1],
            ...,
            [1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1]]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_Q</span></div><div class='xr-var-dims'>(time, dim_6)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0253 0.05714 ... 32.56 32.59</div><input id='attrs-278f1541-1853-4141-84fe-4ce5f386ae3f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-278f1541-1853-4141-84fe-4ce5f386ae3f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4f4e51fb-f90a-4721-bc08-435a1038350f' class='xr-var-data-in' type='checkbox'><label for='data-4f4e51fb-f90a-4721-bc08-435a1038350f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[2.53048628e-02, 5.71350587e-02, 8.89652545e-02, ...,
            3.25239349e+01, 3.25557651e+01, 3.25875953e+01]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_I</span></div><div class='xr-var-dims'>(time, dim_7)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>17.449076 15.25509 ... 0.0 0.0</div><input id='attrs-fbff9567-67ef-40d5-9311-ed7192dde03f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-fbff9567-67ef-40d5-9311-ed7192dde03f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-240b5616-f5bc-471a-822b-39fe16171475' class='xr-var-data-in' type='checkbox'><label for='data-240b5616-f5bc-471a-822b-39fe16171475' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[17.449076, 15.25509 , 17.243057, ...,  0.      ,  0.      ,
             0.      ]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_max</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>21331.768</div><input id='attrs-32e4fa6e-3c64-4724-8285-5c8b4611838d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-32e4fa6e-3c64-4724-8285-5c8b4611838d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6c7325fc-81ee-49f5-a04e-4c52b77bf1b4' class='xr-var-data-in' type='checkbox'><label for='data-6c7325fc-81ee-49f5-a04e-4c52b77bf1b4' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([21331.768], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_argmax</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>3.081</div><input id='attrs-c6fdba1c-984f-4dd3-baa2-cefa569a0a27' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c6fdba1c-984f-4dd3-baa2-cefa569a0a27' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-33ee0e16-f401-4506-b97f-e96d590628fd' class='xr-var-data-in' type='checkbox'><label for='data-33ee0e16-f401-4506-b97f-e96d590628fd' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([3.08100367])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>iq_Q</span></div><div class='xr-var-dims'>(time, dim_8)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.03183 0.06366 ... 23.97 24.0</div><input id='attrs-6e6c02c3-8722-429b-9451-dbf4308b0576' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6e6c02c3-8722-429b-9451-dbf4308b0576' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-eea51e87-071d-4570-91f3-1ec4de0b159c' class='xr-var-data-in' type='checkbox'><label for='data-eea51e87-071d-4570-91f3-1ec4de0b159c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        ,  0.0318302 ,  0.06366039,  0.09549059,  0.12732078,
             0.15915098,  0.19098118,  0.22281137,  0.25464157,  0.28647176,
             0.31830196,  0.35013215,  0.38196235,  0.41379255,  0.44562274,
             0.47745294,  0.50928313,  0.54111333,  0.57294353,  0.60477372,
             0.63660392,  0.66843411,  0.70026431,  0.73209451,  0.7639247 ,
             0.7957549 ,  0.82758509,  0.85941529,  0.89124548,  0.92307568,
             0.95490588,  0.98673607,  1.01856627,  1.05039646,  1.08222666,
             1.11405686,  1.14588705,  1.17771725,  1.20954744,  1.24137764,
             1.27320784,  1.30503803,  1.33686823,  1.36869842,  1.40052862,
             1.43235882,  1.46418901,  1.49601921,  1.5278494 ,  1.5596796 ,
             1.59150979,  1.62333999,  1.65517019,  1.68700038,  1.71883058,
             1.75066077,  1.78249097,  1.81432117,  1.84615136,  1.87798156,
             1.90981175,  1.94164195,  1.97347215,  2.00530234,  2.03713254,
             2.06896273,  2.10079293,  2.13262312,  2.16445332,  2.19628352,
             2.22811371,  2.25994391,  2.2917741 ,  2.3236043 ,  2.3554345 ,
             2.38726469,  2.41909489,  2.45092508,  2.48275528,  2.51458548,
             2.54641567,  2.57824587,  2.61007606,  2.64190626,  2.67373645,
             2.70556665,  2.73739685,  2.76922704,  2.80105724,  2.83288743,
             2.86471763,  2.89654783,  2.92837802,  2.96020822,  2.99203841,
             3.02386861,  3.05569881,  3.087529  ,  3.1193592 ,  3.15118939,
    ...
            20.84877831, 20.8806085 , 20.9124387 , 20.9442689 , 20.97609909,
            21.00792929, 21.03975948, 21.07158968, 21.10341988, 21.13525007,
            21.16708027, 21.19891046, 21.23074066, 21.26257085, 21.29440105,
            21.32623125, 21.35806144, 21.38989164, 21.42172183, 21.45355203,
            21.48538223, 21.51721242, 21.54904262, 21.58087281, 21.61270301,
            21.64453321, 21.6763634 , 21.7081936 , 21.74002379, 21.77185399,
            21.80368418, 21.83551438, 21.86734458, 21.89917477, 21.93100497,
            21.96283516, 21.99466536, 22.02649556, 22.05832575, 22.09015595,
            22.12198614, 22.15381634, 22.18564654, 22.21747673, 22.24930693,
            22.28113712, 22.31296732, 22.34479751, 22.37662771, 22.40845791,
            22.4402881 , 22.4721183 , 22.50394849, 22.53577869, 22.56760889,
            22.59943908, 22.63126928, 22.66309947, 22.69492967, 22.72675987,
            22.75859006, 22.79042026, 22.82225045, 22.85408065, 22.88591085,
            22.91774104, 22.94957124, 22.98140143, 23.01323163, 23.04506182,
            23.07689202, 23.10872222, 23.14055241, 23.17238261, 23.2042128 ,
            23.236043  , 23.2678732 , 23.29970339, 23.33153359, 23.36336378,
            23.39519398, 23.42702418, 23.45885437, 23.49068457, 23.52251476,
            23.55434496, 23.58617515, 23.61800535, 23.64983555, 23.68166574,
            23.71349594, 23.74532613, 23.77715633, 23.80898653, 23.84081672,
            23.87264692, 23.90447711, 23.93630731, 23.96813751, 23.9999677 ]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>iq_I</span></div><div class='xr-var-dims'>(time, dim_9)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>17.45 17.0 15.66 ... 74.1 73.68</div><input id='attrs-a8f1c056-7361-46d3-a73d-52e8b45136eb' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a8f1c056-7361-46d3-a73d-52e8b45136eb' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ebd0531b-a03b-443c-9bd6-c7e15193853f' class='xr-var-data-in' type='checkbox'><label for='data-ebd0531b-a03b-443c-9bd6-c7e15193853f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[1.74490757e+01, 1.69992987e+01, 1.56626320e+01, 1.74703867e+01,
            1.82314899e+01, 1.77723650e+01, 1.79923798e+01, 1.86504720e+01,
            1.86278119e+01, 2.02567210e+01, 2.41870058e+01, 3.32590795e+01,
            4.91376314e+01, 7.30356792e+01, 9.84936908e+01, 1.18458734e+02,
            1.37275093e+02, 1.60926731e+02, 1.87243910e+02, 2.09734490e+02,
            2.20428456e+02, 2.29835892e+02, 2.37006081e+02, 2.43149251e+02,
            2.48993769e+02, 2.55153101e+02, 2.59127294e+02, 2.64476241e+02,
            2.68652539e+02, 2.72060140e+02, 2.76712961e+02, 2.82302800e+02,
            2.87209671e+02, 2.93951986e+02, 3.00859860e+02, 3.08066882e+02,
            3.16258739e+02, 3.23977231e+02, 3.30552314e+02, 3.38680625e+02,
            3.46476725e+02, 3.54501546e+02, 3.59268364e+02, 3.55397755e+02,
            3.46637764e+02, 3.36138057e+02, 3.25597659e+02, 3.16246679e+02,
            3.06201998e+02, 2.95923148e+02, 2.87079741e+02, 2.80166792e+02,
            2.74960669e+02, 2.71866420e+02, 2.69234512e+02, 2.67884610e+02,
            2.66130365e+02, 2.64776255e+02, 2.63726726e+02, 2.62212858e+02,
            2.58381261e+02, 2.53875055e+02, 2.49515595e+02, 2.44848096e+02,
            2.40525781e+02, 2.37253478e+02, 2.34127167e+02, 2.31202783e+02,
            2.28390219e+02, 2.26667417e+02, 2.25341003e+02, 2.23721918e+02,
            2.22190254e+02, 2.21914465e+02, 2.22466176e+02, 2.24527675e+02,
            2.27023414e+02, 2.29708290e+02, 2.32981781e+02, 2.36155545e+02,
    ...
            9.74582451e+01, 9.95953449e+01, 1.00558303e+02, 9.95161601e+01,
            9.74455144e+01, 9.52782035e+01, 9.36979739e+01, 9.26285455e+01,
            9.20636392e+01, 9.18108913e+01, 9.24163763e+01, 9.38463873e+01,
            9.56380139e+01, 9.68500311e+01, 9.57089248e+01, 9.31999562e+01,
            9.17490841e+01, 9.17065724e+01, 9.32667132e+01, 9.55807180e+01,
            9.62349107e+01, 9.39821180e+01, 9.08120928e+01, 8.85367548e+01,
            8.75534450e+01, 8.69651889e+01, 8.66846185e+01, 8.63809746e+01,
            8.63784877e+01, 8.64525122e+01, 8.66992378e+01, 8.66280788e+01,
            8.62216662e+01, 8.54948699e+01, 8.53092902e+01, 8.53419303e+01,
            8.59511670e+01, 8.72290927e+01, 8.85321548e+01, 8.94252400e+01,
            8.90326335e+01, 8.71715986e+01, 8.48951726e+01, 8.34520534e+01,
            8.28345377e+01, 8.26872545e+01, 8.29400187e+01, 8.35994634e+01,
            8.39557361e+01, 8.36291483e+01, 8.25534566e+01, 8.20855279e+01,
            8.26846879e+01, 8.38482739e+01, 8.53235981e+01, 8.55899325e+01,
            8.41952229e+01, 8.20712543e+01, 8.03228259e+01, 7.93475595e+01,
            7.86968165e+01, 7.81825859e+01, 7.78836842e+01, 7.80504384e+01,
            7.81602998e+01, 7.78745627e+01, 7.75449953e+01, 7.73764532e+01,
            7.73500989e+01, 7.77641318e+01, 7.88876575e+01, 8.01621440e+01,
            8.06063787e+01, 7.95783767e+01, 7.80683545e+01, 7.64007970e+01,
            7.48447155e+01, 7.40994861e+01, 7.36818762e+01]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>sq_Q</span></div><div class='xr-var-dims'>(time, dim_10)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.03183 0.06366 ... 21.96 21.99</div><input id='attrs-4479519c-ce37-4aa6-9296-7845c4b7ce84' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4479519c-ce37-4aa6-9296-7845c4b7ce84' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-24f12484-7b5e-4de2-ba6d-fc3b359cacaa' class='xr-var-data-in' type='checkbox'><label for='data-24f12484-7b5e-4de2-ba6d-fc3b359cacaa' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        ,  0.0318302 ,  0.06366039,  0.09549059,  0.12732078,
             0.15915098,  0.19098118,  0.22281137,  0.25464157,  0.28647176,
             0.31830196,  0.35013215,  0.38196235,  0.41379255,  0.44562274,
             0.47745294,  0.50928313,  0.54111333,  0.57294353,  0.60477372,
             0.63660392,  0.66843411,  0.70026431,  0.73209451,  0.7639247 ,
             0.7957549 ,  0.82758509,  0.85941529,  0.89124548,  0.92307568,
             0.95490588,  0.98673607,  1.01856627,  1.05039646,  1.08222666,
             1.11405686,  1.14588705,  1.17771725,  1.20954744,  1.24137764,
             1.27320784,  1.30503803,  1.33686823,  1.36869842,  1.40052862,
             1.43235882,  1.46418901,  1.49601921,  1.5278494 ,  1.5596796 ,
             1.59150979,  1.62333999,  1.65517019,  1.68700038,  1.71883058,
             1.75066077,  1.78249097,  1.81432117,  1.84615136,  1.87798156,
             1.90981175,  1.94164195,  1.97347215,  2.00530234,  2.03713254,
             2.06896273,  2.10079293,  2.13262312,  2.16445332,  2.19628352,
             2.22811371,  2.25994391,  2.2917741 ,  2.3236043 ,  2.3554345 ,
             2.38726469,  2.41909489,  2.45092508,  2.48275528,  2.51458548,
             2.54641567,  2.57824587,  2.61007606,  2.64190626,  2.67373645,
             2.70556665,  2.73739685,  2.76922704,  2.80105724,  2.83288743,
             2.86471763,  2.89654783,  2.92837802,  2.96020822,  2.99203841,
             3.02386861,  3.05569881,  3.087529  ,  3.1193592 ,  3.15118939,
    ...
            18.93896655, 18.97079675, 19.00262695, 19.03445714, 19.06628734,
            19.09811753, 19.12994773, 19.16177793, 19.19360812, 19.22543832,
            19.25726851, 19.28909871, 19.32092891, 19.3527591 , 19.3845893 ,
            19.41641949, 19.44824969, 19.48007988, 19.51191008, 19.54374028,
            19.57557047, 19.60740067, 19.63923086, 19.67106106, 19.70289126,
            19.73472145, 19.76655165, 19.79838184, 19.83021204, 19.86204224,
            19.89387243, 19.92570263, 19.95753282, 19.98936302, 20.02119321,
            20.05302341, 20.08485361, 20.1166838 , 20.148514  , 20.18034419,
            20.21217439, 20.24400459, 20.27583478, 20.30766498, 20.33949517,
            20.37132537, 20.40315557, 20.43498576, 20.46681596, 20.49864615,
            20.53047635, 20.56230655, 20.59413674, 20.62596694, 20.65779713,
            20.68962733, 20.72145752, 20.75328772, 20.78511792, 20.81694811,
            20.84877831, 20.8806085 , 20.9124387 , 20.9442689 , 20.97609909,
            21.00792929, 21.03975948, 21.07158968, 21.10341988, 21.13525007,
            21.16708027, 21.19891046, 21.23074066, 21.26257085, 21.29440105,
            21.32623125, 21.35806144, 21.38989164, 21.42172183, 21.45355203,
            21.48538223, 21.51721242, 21.54904262, 21.58087281, 21.61270301,
            21.64453321, 21.6763634 , 21.7081936 , 21.74002379, 21.77185399,
            21.80368418, 21.83551438, 21.86734458, 21.89917477, 21.93100497,
            21.96283516, 21.99466536]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>sq_S</span></div><div class='xr-var-dims'>(time, dim_11)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.441 1.42 1.399 ... 1.014 0.9995</div><input id='attrs-ebde66d5-b267-4f10-bb76-3adb83689c33' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ebde66d5-b267-4f10-bb76-3adb83689c33' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-df7a7fdb-965e-4238-a53a-0ae8c89297c1' class='xr-var-data-in' type='checkbox'><label for='data-df7a7fdb-965e-4238-a53a-0ae8c89297c1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[1.44081866, 1.41981957, 1.39906439, 1.37918811, 1.35951973,
            1.34002596, 1.32100367, 1.30240962, 1.28405999, 1.26632305,
            1.24929995, 1.23344626, 1.2190332 , 1.20626319, 1.19409556,
            1.18138043, 1.16881716, 1.15738424, 1.14673059, 1.13578413,
            1.12320851, 1.11073121, 1.09818604, 1.08576812, 1.07359461,
            1.0617655 , 1.04984921, 1.03844949, 1.02712475, 1.01593813,
            1.00523673, 0.99496631, 0.98483846, 0.97529748, 0.96604566,
            0.95710431, 0.94859614, 0.94025376, 0.93194827, 0.92417391,
            0.91658006, 0.90926811, 0.90157293, 0.89244777, 0.88257606,
            0.87254518, 0.86267617, 0.85320734, 0.84376577, 0.83443641,
            0.82555113, 0.81721333, 0.80938256, 0.80214693, 0.79517008,
            0.78862283, 0.78215207, 0.77592404, 0.76991721, 0.76396392,
            0.75765499, 0.75133653, 0.74518394, 0.73909356, 0.7332078 ,
            0.72768543, 0.72232276, 0.71713077, 0.71208699, 0.7074183 ,
            0.70296468, 0.69856206, 0.69429746, 0.69045133, 0.68692431,
            0.68388661, 0.6810788 , 0.67844031, 0.67607082, 0.67379743,
            0.6716424 , 0.66968651, 0.66804367, 0.66669048, 0.66559618,
            0.66467602, 0.66406079, 0.66372731, 0.66415789, 0.66613362,
            0.67066807, 0.6802721 , 0.70308678, 0.77184812, 1.03740991,
            2.04527338, 4.48513999, 6.63947769, 5.20172815, 2.35408837,
    ...
            0.95604705, 0.9608355 , 0.97390518, 1.00217805, 1.04258786,
            1.07878673, 1.09810373, 1.1034093 , 1.0816646 , 1.03393221,
            0.98897848, 0.96868041, 0.96270436, 0.960861  , 0.96240767,
            0.97294368, 0.99394702, 1.01700675, 1.02282207, 1.00223255,
            0.97631878, 0.96403137, 0.96488497, 0.97781867, 0.99977995,
            1.01749416, 1.01058087, 0.98596325, 0.96634679, 0.95838788,
            0.95555419, 0.95408012, 0.95406125, 0.9546458 , 0.95779567,
            0.96062807, 0.96592607, 0.97321322, 0.97653979, 0.97596385,
            0.97378001, 0.9781229 , 0.99511825, 1.03065644, 1.08220202,
            1.11863088, 1.1127029 , 1.07823281, 1.04348347, 1.0134038 ,
            0.99134974, 0.98292983, 0.98073362, 0.98122166, 0.98529243,
            0.99812924, 1.01400698, 1.02347691, 1.01567839, 0.99909043,
            0.99000914, 0.99295082, 1.00671051, 1.03091632, 1.05208522,
            1.05712293, 1.04544024, 1.02847238, 1.00801862, 0.9911789 ,
            0.9822223 , 0.97927628, 0.97952865, 0.98164694, 0.98755204,
            0.9943492 , 0.99752411, 0.99207041, 0.98411696, 0.9815523 ,
            0.98510601, 0.99546581, 1.01092193, 1.01909779, 1.01467583,
            1.00370828, 0.99204683, 0.98404261, 0.9792457 , 0.97764904,
            0.97804693, 0.98398864, 0.99531282, 1.00906291, 1.01911829,
            1.01382084, 0.99948833]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>fq_Q</span></div><div class='xr-var-dims'>(time, dim_12)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.03183 0.06366 ... 21.96 21.99</div><input id='attrs-8b9c9e74-e841-4cee-82fc-5d9f8b169f89' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8b9c9e74-e841-4cee-82fc-5d9f8b169f89' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-847250f0-a26a-4f1f-8dae-45699d58f177' class='xr-var-data-in' type='checkbox'><label for='data-847250f0-a26a-4f1f-8dae-45699d58f177' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        ,  0.0318302 ,  0.06366039,  0.09549059,  0.12732078,
             0.15915098,  0.19098118,  0.22281137,  0.25464157,  0.28647176,
             0.31830196,  0.35013215,  0.38196235,  0.41379255,  0.44562274,
             0.47745294,  0.50928313,  0.54111333,  0.57294353,  0.60477372,
             0.63660392,  0.66843411,  0.70026431,  0.73209451,  0.7639247 ,
             0.7957549 ,  0.82758509,  0.85941529,  0.89124548,  0.92307568,
             0.95490588,  0.98673607,  1.01856627,  1.05039646,  1.08222666,
             1.11405686,  1.14588705,  1.17771725,  1.20954744,  1.24137764,
             1.27320784,  1.30503803,  1.33686823,  1.36869842,  1.40052862,
             1.43235882,  1.46418901,  1.49601921,  1.5278494 ,  1.5596796 ,
             1.59150979,  1.62333999,  1.65517019,  1.68700038,  1.71883058,
             1.75066077,  1.78249097,  1.81432117,  1.84615136,  1.87798156,
             1.90981175,  1.94164195,  1.97347215,  2.00530234,  2.03713254,
             2.06896273,  2.10079293,  2.13262312,  2.16445332,  2.19628352,
             2.22811371,  2.25994391,  2.2917741 ,  2.3236043 ,  2.3554345 ,
             2.38726469,  2.41909489,  2.45092508,  2.48275528,  2.51458548,
             2.54641567,  2.57824587,  2.61007606,  2.64190626,  2.67373645,
             2.70556665,  2.73739685,  2.76922704,  2.80105724,  2.83288743,
             2.86471763,  2.89654783,  2.92837802,  2.96020822,  2.99203841,
             3.02386861,  3.05569881,  3.087529  ,  3.1193592 ,  3.15118939,
    ...
            18.93896655, 18.97079675, 19.00262695, 19.03445714, 19.06628734,
            19.09811753, 19.12994773, 19.16177793, 19.19360812, 19.22543832,
            19.25726851, 19.28909871, 19.32092891, 19.3527591 , 19.3845893 ,
            19.41641949, 19.44824969, 19.48007988, 19.51191008, 19.54374028,
            19.57557047, 19.60740067, 19.63923086, 19.67106106, 19.70289126,
            19.73472145, 19.76655165, 19.79838184, 19.83021204, 19.86204224,
            19.89387243, 19.92570263, 19.95753282, 19.98936302, 20.02119321,
            20.05302341, 20.08485361, 20.1166838 , 20.148514  , 20.18034419,
            20.21217439, 20.24400459, 20.27583478, 20.30766498, 20.33949517,
            20.37132537, 20.40315557, 20.43498576, 20.46681596, 20.49864615,
            20.53047635, 20.56230655, 20.59413674, 20.62596694, 20.65779713,
            20.68962733, 20.72145752, 20.75328772, 20.78511792, 20.81694811,
            20.84877831, 20.8806085 , 20.9124387 , 20.9442689 , 20.97609909,
            21.00792929, 21.03975948, 21.07158968, 21.10341988, 21.13525007,
            21.16708027, 21.19891046, 21.23074066, 21.26257085, 21.29440105,
            21.32623125, 21.35806144, 21.38989164, 21.42172183, 21.45355203,
            21.48538223, 21.51721242, 21.54904262, 21.58087281, 21.61270301,
            21.64453321, 21.6763634 , 21.7081936 , 21.74002379, 21.77185399,
            21.80368418, 21.83551438, 21.86734458, 21.89917477, 21.93100497,
            21.96283516, 21.99466536]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>fq_F</span></div><div class='xr-var-dims'>(time, dim_13)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.01336 ... 0.3035 -0.01125</div><input id='attrs-5e4b03b0-7ddf-4537-90e0-cbf663979fbe' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5e4b03b0-7ddf-4537-90e0-cbf663979fbe' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-de6a1417-4720-49d8-8157-e4156f35a933' class='xr-var-data-in' type='checkbox'><label for='data-de6a1417-4720-49d8-8157-e4156f35a933' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.00000000e+00,  1.33629391e-02,  2.54045954e-02,
             3.62088950e-02,  4.57743343e-02,  5.41154638e-02,
             6.13056589e-02,  6.73803015e-02,  7.23334823e-02,
             7.62940329e-02,  7.93526608e-02,  8.17370412e-02,
             8.36624360e-02,  8.53501688e-02,  8.64933963e-02,
             8.66006176e-02,  8.59757348e-02,  8.51627097e-02,
             8.40683431e-02,  8.21186759e-02,  7.84350187e-02,
             7.40165180e-02,  6.87561784e-02,  6.27903716e-02,
             5.62207429e-02,  4.91502014e-02,  4.12544627e-02,
             3.30440770e-02,  2.41748150e-02,  1.47120962e-02,
             5.00058434e-03, -4.96692403e-03, -1.54430380e-02,
            -2.59474382e-02, -3.67462968e-02, -4.77882392e-02,
            -5.89030154e-02, -7.03641739e-02, -8.23117904e-02,
            -9.41288150e-02, -1.06210922e-01, -1.18408565e-01,
            -1.31584024e-01, -1.47206571e-01, -1.64455595e-01,
            -1.82561031e-01, -2.01068042e-01, -2.19604632e-01,
            -2.38702380e-01, -2.58226155e-01, -2.77637090e-01,
            -2.96724903e-01, -3.15504311e-01, -3.33778201e-01,
            -3.52067924e-01, -3.70049715e-01, -3.88311959e-01,
            -4.06545757e-01, -4.24767648e-01, -4.43271399e-01,
    ...
            -4.72688425e-01, -4.85057684e-01, -5.29962934e-01,
            -4.42880122e-01, -9.89815414e-02,  6.22560762e-01,
             1.67194749e+00,  2.41666826e+00,  2.29949473e+00,
             1.59868632e+00,  8.89968226e-01,  2.74759667e-01,
            -1.77593889e-01, -3.51001991e-01, -3.96774531e-01,
            -3.87321521e-01, -3.03825923e-01, -3.87052387e-02,
             2.90244954e-01,  4.87223120e-01,  3.25877140e-01,
            -1.89344236e-02, -2.08297292e-01, -1.47191084e-01,
             1.40333078e-01,  6.47519697e-01,  1.09254479e+00,
             1.20003453e+00,  9.56051825e-01,  5.99958380e-01,
             1.69220264e-01, -1.86436116e-01, -3.76302033e-01,
            -4.39320237e-01, -4.34621895e-01, -3.90233279e-01,
            -2.65071758e-01, -1.20510201e-01, -5.28801902e-02,
            -1.69613113e-01, -3.40242116e-01, -3.95768588e-01,
            -3.20003121e-01, -9.75630791e-02,  2.35357129e-01,
             4.12146918e-01,  3.17184350e-01,  8.02640466e-02,
            -1.72395852e-01, -3.46406194e-01, -4.51198969e-01,
            -4.86621825e-01, -4.78657784e-01, -3.49616217e-01,
            -1.02496196e-01,  1.98470188e-01,  4.19283288e-01,
             3.03544788e-01, -1.12540794e-02]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_r</span></div><div class='xr-var-dims'>(time, dim_14)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.01 0.02 ... 29.98 29.99 30.0</div><input id='attrs-9bd24676-5259-4b7a-9cb9-aadc19250466' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9bd24676-5259-4b7a-9cb9-aadc19250466' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b856c170-c29d-4566-950d-159651d008f4' class='xr-var-data-in' type='checkbox'><label for='data-b856c170-c29d-4566-950d-159651d008f4' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[0.000e+00, 1.000e-02, 2.000e-02, ..., 2.998e+01, 2.999e+01,
            3.000e+01]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_G</span></div><div class='xr-var-dims'>(time, dim_15)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.003567 0.006975 ... 1.4 1.455</div><input id='attrs-4821d291-5bd3-4607-aa1e-0e31ef1d92aa' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4821d291-5bd3-4607-aa1e-0e31ef1d92aa' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-18d76aa5-050e-446b-ac84-6e5f92dc8ae0' class='xr-var-data-in' type='checkbox'><label for='data-18d76aa5-050e-446b-ac84-6e5f92dc8ae0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[0.        , 0.0035669 , 0.00697492, ..., 1.33294076, 1.39995837,
            1.45483018]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_max</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>7.417</div><input id='attrs-a2e83c04-9eea-4b74-b5ce-43a145f370fe' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a2e83c04-9eea-4b74-b5ce-43a145f370fe' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a9e84575-d578-45fc-a2b2-b3ec04b9df1a' class='xr-var-data-in' type='checkbox'><label for='data-a9e84575-d578-45fc-a2b2-b3ec04b9df1a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([7.41703315])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_argmax</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>6.59</div><input id='attrs-bce209a0-4ed6-482a-bdef-48943b486c52' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-bce209a0-4ed6-482a-bdef-48943b486c52' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ea88a897-ce59-4f58-a66d-0a082e43308f' class='xr-var-data-in' type='checkbox'><label for='data-ea88a897-ce59-4f58-a66d-0a082e43308f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([6.59])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>seq_num</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-8f114cdf-5cf0-4667-96fa-539ccb85f208' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8f114cdf-5cf0-4667-96fa-539ccb85f208' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-99e94059-31d9-46fe-a7ea-4579122e4128' class='xr-var-data-in' type='checkbox'><label for='data-99e94059-31d9-46fe-a7ea-4579122e4128' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>uid</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U36</div><div class='xr-var-preview xr-preview'>&#x27;714d3474-7f29-4ee0-bee3-fe5d217...</div><input id='attrs-7c46d03a-a855-4b0a-afab-ea03c904f593' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7c46d03a-a855-4b0a-afab-ea03c904f593' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-94cd55a3-96e9-4c69-af19-1286fbc8b626' class='xr-var-data-in' type='checkbox'><label for='data-94cd55a3-96e9-4c69-af19-1286fbc8b626' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;714d3474-7f29-4ee0-bee3-fe5d2171daea&#x27;], dtype=&#x27;&lt;U36&#x27;)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-db5e2baf-7cb1-42ba-a706-9ce94ad20695' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-db5e2baf-7cb1-42ba-a706-9ce94ad20695' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>
    <br />
    <br />

Here, we plot the most important part of data, that is, the reduced pair distribution function.


.. code-block:: default


    import matplotlib.pyplot as plt

    plt.plot(an_data["gr_r"][0], an_data["gr_G"][0])




.. image:: /tutorials2/images/sphx_glr_plot_xpd_analyzer_002.png
    :alt: plot xpd analyzer
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    [<matplotlib.lines.Line2D object at 0x7fa4b04496d0>]



Change settings
^^^^^^^^^^^^^^^

We can change all the settings for the analyzer except the visualization settings
before or after the analyzer is created.
For example, we think that the ``qmax`` in section ``TRANSFORMATION SETTING``
is slightly larger than the ideal and thus we decrease it to 20 inverse angstrom.


.. code-block:: default


    config.set("TRANSFORMATION SETTING", "qmax", '20')








We can also use another way.


.. code-block:: default


    config["TRANSFORMATION SETTING"]["qmax"] = '20'








Then, we just need to run ``analyzer.analyze(run)``.

Export the processed data to files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Besides saving the metadata and data in the database, we can also export them in files at the same time.
For example, we run the code blow to let the analyzer export the processed data into the ``~/my_folder``.


.. code-block:: default


    config["FUNCTIONALITY"]["export_files"] = "True"
    config["FILE SYSTEM"]["tiff_base"] = "~/my_folder"








Then, we need to build the analyzer again ``analyzer = XPDAnalyzer(config)`` to make the functionality
take effect and rerun the analysis ``analyzer.analyze(run)``.
The detail of what the data will be like is introduced in :ref:`xpd-server-data`.

Live visualization
^^^^^^^^^^^^^^^^^^

If you would like live visualization of the processed data, run the code below to run on the functionality.


.. code-block:: default


    config["FUNCTIONALITY"]["visualize_data"] = "True"








Then, we need to build the analyzer again ``analyzer = XPDAnalyzer(config)`` to make the functionality
take effect and rerun the analysis ``analyzer.analyze(run)``.
The detail of what the figures will be like is introduced in :ref:`xpd-server-figures`.

Replay the data processing
^^^^^^^^^^^^^^^^^^^^^^^^^^

We can replay the analysis process according to the metadata and data in the analysis run.


.. code-block:: default


    from pdfstream.analyzers.xpd_analyzer import replay

    config2, analyzer2 = replay(an_run)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Warning: a temporary db is created for an db. It will be destroy at the end of the session.




The ``confgi2`` and ``analyzer2`` have the same settings as the ``config`` and ``analyzer``
except the databases.
It is because we uses two special temporary databases for the demonstration.
You will not encounter the problem if you are using permanent database in catalog.


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  14.490 seconds)


.. _sphx_glr_download_tutorials2_plot_xpd_analyzer.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_xpd_analyzer.py <plot_xpd_analyzer.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_xpd_analyzer.ipynb <plot_xpd_analyzer.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
