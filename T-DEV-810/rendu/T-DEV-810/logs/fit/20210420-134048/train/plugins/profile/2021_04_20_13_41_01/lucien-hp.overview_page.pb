?	4???E??@4???E??@!4???E??@	B?nv?ll?B?nv?ll?!B?nv?ll?"e
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails$4???E??@,??zM??A???|??@Y??d????*	#???D?5A2~
GIterator::Model::MaxIntraOpParallelism::Prefetch::FlatMap[0]::Generator?$D)
?@!??6???X@)?$D)
?@1??6???X@:Preprocessing2g
0Iterator::Model::MaxIntraOpParallelism::Prefetchb?7?W???!?T??/f?)b?7?W???1?T??/f?:Preprocessing2]
&Iterator::Model::MaxIntraOpParallelism?J?.????!vi>6u?)M??f?ס?1{?~(?<d?:Preprocessing2F
Iterator::ModelX?<?????!?$?O??w?) <?Bus??1mw-2?C?:Preprocessing2p
9Iterator::Model::MaxIntraOpParallelism::Prefetch::FlatMapP???0
?@!??nA??X@)jkD0.}?1?'Q?p?@?:Preprocessing:?
]Enqueuing data: you may want to combine small input data chunks into fewer but larger chunks.
?Data preprocessing: you may increase num_parallel_calls in <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#map" target="_blank">Dataset map()</a> or preprocess the data OFFLINE.
?Reading data from files in advance: you may tune parameters in the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch size</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave cycle_length</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer_size</a>)
?Reading data from files on demand: you should read data IN ADVANCE using the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer</a>)
?Other data reading or processing: you may consider using the <a href="https://www.tensorflow.org/programmers_guide/datasets" target="_blank">tf.data API</a> (if you are not using it now)?
:type.googleapis.com/tensorflow.profiler.BottleneckAnalysis?
device?Your program is NOT input-bound because only 0.0% of the total step time sampled is waiting for input. Therefore, you should focus on reducing other time.no*no9C?nv?ll?I#o&??X@Zno#You may skip the rest of this page.B?
@type.googleapis.com/tensorflow.profiler.GenericStepTimeBreakdown?
	,??zM??,??zM??!,??zM??      ??!       "      ??!       *      ??!       2	???|??@???|??@!???|??@:      ??!       B      ??!       J	??d??????d????!??d????R      ??!       Z	??d??????d????!??d????b      ??!       JCPU_ONLYYC?nv?ll?b q#o&??X@Y      Y@qc??6e\?"?
device?Your program is NOT input-bound because only 0.0% of the total step time sampled is waiting for input. Therefore, you should focus on reducing other time.b
`input_pipeline_analyzer (especially Section 3 for the breakdown of input operations on the Host)Q
Otf_data_bottleneck_analysis (find the bottleneck in the tf.data input pipeline)m
ktrace_viewer (look at the activities on the timeline of each Host Thread near the bottom of the trace view)"T
Rtensorflow_stats (identify the time-consuming operations executed on the CPU_ONLY)"Z
Xtrace_viewer (look at the activities on the timeline of each CPU_ONLY in the trace view)*?
?<a href="https://www.tensorflow.org/guide/data_performance_analysis" target="_blank">Analyze tf.data performance with the TF Profiler</a>*y
w<a href="https://www.tensorflow.org/guide/data_performance" target="_blank">Better performance with the tf.data API</a>2M
=type.googleapis.com/tensorflow.profiler.GenericRecommendation
nono2no:
Refer to the TF2 Profiler FAQ2"CPU: B 