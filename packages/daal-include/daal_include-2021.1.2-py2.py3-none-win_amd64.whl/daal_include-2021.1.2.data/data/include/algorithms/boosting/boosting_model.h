/* file: boosting_model.h */
/*******************************************************************************
* Copyright 2014-2020 Intel Corporation
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

/*
//++
//  Implementation of the base class defining Boosting algorithm model.
//--
*/

#ifndef __BOOSTING_MODEL_H__
#define __BOOSTING_MODEL_H__

#include "algorithms/weak_learner/weak_learner_model.h"
#include "algorithms/weak_learner/weak_learner_training_batch.h"
#include "algorithms/weak_learner/weak_learner_predict.h"
#include "algorithms/stump/stump_training_batch.h"
#include "algorithms/stump/stump_predict.h"
#include "algorithms/classifier/classifier_model.h"

namespace daal
{
namespace algorithms
{
/**
 * \brief Contains classes of boosting classification algorithms
 */
namespace boosting
{
/**
 * \brief Contains version 1.0 of Intel(R) oneAPI Data Analytics Library interface.
 */
namespace interface1
{
/**
 * @ingroup boosting
 * @{
 */
/**
 * <a name="DAAL-STRUCT-ALGORITHMS__BOOSTING__PARAMETER"></a>
* \brief %Base class for parameters of the %boosting algorithm
 *
 * \snippet boosting/boosting_model.h Parameter source code
 */
/* [Parameter source code] */
struct DAAL_EXPORT Parameter : public classifier::interface1::Parameter
{
    /** Default constructor. Sets the decision stump as the default weak learner */
    Parameter();

    /**
     * Constructs %boosting algorithm parameters from weak learner training and prediction algorithms
     * \param[in] wlTrainForParameter       Pointer to the training algorithm of the weak learner
     * \param[in] wlPredictForParameter     Pointer to the prediction algorithm of the weak learner
     */
    Parameter(const services::SharedPtr<weak_learner::training::Batch> & wlTrainForParameter,
              const services::SharedPtr<weak_learner::prediction::Batch> & wlPredictForParameter);

    /** Copy constructor */
    Parameter(const Parameter & other)
        : classifier::interface1::Parameter(), weakLearnerTraining(other.weakLearnerTraining), weakLearnerPrediction(other.weakLearnerPrediction)
    {}

    /** The algorithm for weak learner model training */
    services::SharedPtr<weak_learner::training::Batch> weakLearnerTraining;

    /** The algorithm for prediction based on a weak learner model */
    services::SharedPtr<weak_learner::prediction::Batch> weakLearnerPrediction;

    services::Status check() const DAAL_C11_OVERRIDE;
};
/* [Parameter source code] */
/** @} */

/**
 * @ingroup boosting
 * @{
 */
/**
 * <a name="DAAL-CLASS-ALGORITHMS__BOOSTING__MODEL"></a>
* \brief %Base class for %boosting algorithm models.
 *        Contains a collection of weak learner models constructed during training of the %boosting algorithm
 */
class DAAL_EXPORT Model : public classifier::Model
{
public:
    /**
     * Constructs the model trained with the boosting algorithm
     * \param[in] nFeatures Number of features in the dataset
     * \DAAL_DEPRECATED_USE{ Model::create }
     */
    Model(size_t nFeatures = 0) : _nFeatures(nFeatures), _models(new data_management::DataCollection()) {}

    virtual ~Model() {}

    /**
     *  Returns the number of weak learners constructed during training of the %boosting algorithm
     *  \return The number of weak learners
     */
    size_t getNumberOfWeakLearners() const;

    /**
     *  Returns weak learner model constructed during training of the %boosting algorithm
     *  \param[in] idx  Index of the model in the collection
     *  \return Weak Learner model corresponding to the index idx
     */
    weak_learner::ModelPtr getWeakLearnerModel(size_t idx) const;

    /**
     *  Add weak learner model into the %boosting model
     *  \param[in] model Weak learner model to add into collection
     */
    void addWeakLearnerModel(weak_learner::ModelPtr model);

    void clearWeakLearnerModels();

    /**
     *  Retrieves the number of features in the dataset was used on the training stage
     *  \return Number of features in the dataset was used on the training stage
     */
    size_t getNumberOfFeatures() const DAAL_C11_OVERRIDE { return _nFeatures; }

protected:
    size_t _nFeatures;
    data_management::DataCollectionPtr _models;

    template <typename Archive, bool onDeserialize>
    services::Status serialImpl(Archive * arch)
    {
        classifier::Model::serialImpl<Archive, onDeserialize>(arch);
        arch->set(_nFeatures);
        arch->setSharedPtrObj(_models);

        return services::Status();
    }

    Model(size_t nFeatures, services::Status & st);
};
typedef services::SharedPtr<Model> ModelPtr;
/** @} */
} // namespace interface1
using interface1::Parameter;
using interface1::Model;
using interface1::ModelPtr;

} // namespace boosting
} // namespace algorithms
} // namespace daal
#endif // __BOOSTING_MODEL_H__
