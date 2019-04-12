import numpy as np
cimport numpy as np

ctypedef np.int_t VAR_INTDTYPE_t
ctypedef np.float32_t VAR_FLOAT32DTYPE_t
ctypedef np.float64_t VAR_FLOAT64DTYPE_t
ctypedef np.uint8_t VAR_UINT8DTYPE_t

ctypedef np.float_t FLOATDTYPE_t

ctypedef fused variable_in_histogram_type:
    np.ndarray[VAR_FLOAT32DTYPE_t, ndim=1]
    np.ndarray[VAR_FLOAT64DTYPE_t, ndim=1]
    np.ndarray[VAR_UINT8DTYPE_t, ndim=1]
    np.ndarray[VAR_INTDTYPE_t, ndim=1]

cpdef  np.ndarray[FLOATDTYPE_t, ndim =1] getWeightsFromBins(variable_in_histogram_type variable_in_histogram, np.ndarray[FLOATDTYPE_t, ndim = 1] low_edges, np.ndarray[FLOATDTYPE_t, ndim=1] high_edges, np.ndarray[FLOATDTYPE_t, ndim = 1] normalization):
    cdef int maxbin = low_edges.shape[0]
    cdef int tracks = variable_in_histogram.shape[0]
    cdef int i, j
    cdef np.ndarray[FLOATDTYPE_t, ndim =1] weights = np.ones(tracks, dtype = np.float)

    for i in range(maxbin):
        for j in range(tracks):
            if (variable_in_histogram[j] >= low_edges[i]) and (variable_in_histogram[j] < high_edges[i]):
                weights[j] = normalization[i]
    return weights

#cpder np.ndarray[FLOATDTYPE_t, ndim =1] getHighestVariablesPerEvent(variable_in_histogram_type trkIndex, variable_in_histogram_type findMaxOfThis, variable_in_histogram_type weights, int NEvents):
#    cdef float current_max = 0.0
#    cdef int i
#    cdef int eventIndex = 0
#    cdef int ntracks = trkIndex.shape[0]
#    cdef np.ndarray[FLOATDTYPE_t, ndim=1] highestVec = np.zeros(NEvents, dtype=np.float)

#    current_max = findMaxOfThis[0]
#    for i in range(1, ntracks):
#        if trkIndex[i] == 0:
#            highestVec[eventIndex] = current_max
#            eventIndex = eventIndex + 1
#            current_max = 0.0
#        elif current_max < findMaxOfThis[i]:
#            current_max = findMaxOfThis[i]
#
#    return highestVec

        

