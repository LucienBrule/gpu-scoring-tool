# ADR-001: Multiclass GPU Categorizer Architecture

## Status
Proposed

## Context

The current GPU Scoring Tool employs a highly successful binary classifier that achieves perfect performance (1.0 F1-score, ROC-AUC) in distinguishing NVIDIA GPUs from non-GPUs across 2,106 test samples. This binary approach has proven effective for the initial goal of identifying valid GPU listings, but business requirements now call for more granular categorization capabilities.

### Current System Capabilities

- **Binary Classification**: Perfect performance (1.0 precision/recall/F1) on GPU vs non-GPU classification
- **Dataset Scale**: 5,509 GPU samples across 58 unique GPU models in normalized dataset
- **Feature Pipeline**: TF-IDF vectorization with n-grams (1,2) on title and bulk_notes fields
- **Model Architecture**: Logistic Regression with optimized hyperparameters
- **Integration**: Fully integrated into `glyphsieve` pipeline with ML signals in `ml_signal.py`

### Business Need for Multiclass Classification

Current limitations include:
1. **Lack of GPU Family Distinction**: Cannot differentiate between GeForce, Quadro, Tesla, or RTX series
2. **Generation Blindness**: No distinction between RTX 30-series, 40-series, 50-series generations
3. **Performance Tier Ambiguity**: Cannot classify entry-level vs high-end vs professional GPUs
4. **Market Analysis Gaps**: Limited ability to analyze trends by specific GPU categories
5. **Pricing Model Constraints**: Scoring algorithms cannot leverage GPU-specific performance characteristics

### Data Analysis Findings

Analysis of the normalized dataset reveals strong multiclass potential:

**Top GPU Model Distribution:**
- RTX_4000_SFF_ADA: 455 samples (8.3%)
- RTX_4060: 350 samples (6.4%)
- RTX_4070: 328 samples (6.0%)
- RTX_3050: 327 samples (5.9%)
- RTX_4070_TI: 304 samples (5.5%)

**GPU Family Representation:**
- Consumer RTX 40-series: ~1,500 samples
- Consumer RTX 30-series: ~800 samples
- Consumer RTX 50-series: ~400 samples
- Professional/Workstation: ~600 samples
- Legacy GTX series: ~350 samples

This distribution provides sufficient samples for robust multiclass training across major GPU categories.

## Decision

We will implement a **hierarchical multiclass GPU categorizer** using a staged approach that builds upon the existing binary classifier foundation. The system will employ multiple classification tiers to provide granular GPU categorization while maintaining the reliability of the current binary approach.

### Chosen Architecture: Hierarchical Multi-Stage Classification

1. **Stage 1**: Existing binary GPU classifier (is_gpu: True/False)
2. **Stage 2**: GPU family classifier (GeForce, Quadro, Tesla, RTX Professional)
3. **Stage 3**: Generation classifier (RTX 30-series, 40-series, 50-series, etc.)
4. **Stage 4**: Specific model classifier (RTX 4070, RTX 4060 Ti, etc.)

This approach provides:
- **Graceful Degradation**: If later stages fail, earlier classifications remain valid
- **Confidence Propagation**: Each stage provides confidence scores that compound
- **Incremental Rollout**: Stages can be deployed and validated independently
- **Interpretability**: Clear decision path for each classification

## Consequences

### Positive

1. **Enhanced Market Intelligence**: Detailed GPU categorization enables sophisticated market analysis and trend identification
2. **Improved Pricing Models**: GPU-specific performance characteristics can inform more accurate scoring algorithms
3. **Better User Experience**: More precise categorization improves search, filtering, and recommendation capabilities
4. **Competitive Advantage**: Granular GPU classification provides deeper market insights than competitors
5. **Scalable Architecture**: Hierarchical approach allows for easy addition of new GPU families and models
6. **Risk Mitigation**: Multi-stage approach ensures system remains functional even if individual stages fail

### Negative

1. **Increased Complexity**: Multi-stage pipeline requires more sophisticated error handling and monitoring
2. **Training Data Requirements**: Each classification tier requires sufficient labeled samples for robust training
3. **Computational Overhead**: Multiple model inference calls increase latency and resource consumption
4. **Maintenance Burden**: More models require ongoing retraining, evaluation, and deployment management
5. **Label Quality Dependency**: Multiclass accuracy heavily depends on consistent, high-quality labeling
6. **Cold Start Problem**: New GPU models may not have sufficient training data initially

### Neutral

1. **Model Storage**: Additional model artifacts (~200MB per stage) require storage planning
2. **Feature Engineering**: Existing TF-IDF pipeline may need enhancement for multiclass discrimination
3. **Evaluation Complexity**: Multi-stage evaluation requires comprehensive test suites and metrics
4. **Integration Points**: `ml_signal.py` module will need updates to handle hierarchical predictions

## Implementation Plan

### Phase 1: Foundation and Research (Weeks 1-2)
- **Label Hierarchy Design**: Define comprehensive GPU categorization taxonomy
- **Feature Engineering Research**: Investigate enhanced features for multiclass discrimination
- **Data Preparation**: Create labeled datasets for each classification tier
- **Baseline Establishment**: Implement simple multiclass baseline using existing features

**Deliverables:**
- `docs/gpu_taxonomy.md` - Comprehensive GPU categorization hierarchy
- `glyphsieve/ml/data/multiclass_labels.csv` - Labeled training data for all tiers
- `glyphsieve/ml/multiclass_baseline.py` - Initial multiclass implementation

### Phase 2: Stage 2 Implementation - GPU Family Classification (Weeks 3-4)
- **Model Development**: Train GPU family classifier (GeForce, Quadro, Tesla, RTX Professional)
- **Feature Enhancement**: Implement enhanced n-grams, manufacturer detection, price-based features
- **Integration**: Extend `ml_signal.py` to support hierarchical predictions
- **Evaluation**: Comprehensive evaluation with confusion matrices and performance analysis

**Deliverables:**
- `models/gpu_family_classifier.pkl` - Trained family classification model
- `glyphsieve/ml/family_classifier.py` - Family classification implementation
- `models/evaluation/family_evaluation_report.md` - Performance analysis

**Success Criteria:**
- Family classification F1-score ≥ 0.90
- Integration with existing pipeline without performance degradation
- Clear decision boundaries between GPU families

### Phase 3: Stage 3 Implementation - Generation Classification (Weeks 5-6)
- **Generation Taxonomy**: Define RTX series generations (30, 40, 50-series, etc.)
- **Temporal Features**: Implement release date and market timing features
- **Model Training**: Train generation-specific classifiers for each GPU family
- **A/B Testing Framework**: Implement framework for gradual rollout and performance monitoring

**Deliverables:**
- `models/generation_classifiers/` - Generation-specific model artifacts
- `glyphsieve/ml/generation_classifier.py` - Generation classification implementation
- `glyphsieve/ml/ab_testing.py` - A/B testing framework for gradual rollout

**Success Criteria:**
- Generation classification F1-score ≥ 0.85 per family
- Successful A/B test with <5% performance impact on existing pipeline
- Clear temporal boundaries between GPU generations

### Phase 4: Stage 4 Implementation - Specific Model Classification (Weeks 7-8)
- **Model-Specific Features**: Implement VRAM size, performance tier, and specification-based features
- **External Data Integration**: Incorporate GPU specification databases and benchmark data
- **Ensemble Methods**: Implement ensemble approaches combining multiple classification signals
- **Production Deployment**: Full integration with confidence score propagation

**Deliverables:**
- `models/specific_model_classifier.pkl` - Specific model classification system
- `glyphsieve/ml/model_classifier.py` - Model-specific classification implementation
- `glyphsieve/resources/gpu_specifications.yaml` - External GPU specification database

**Success Criteria:**
- Specific model classification F1-score ≥ 0.80
- End-to-end pipeline latency <200ms per prediction
- Confidence score calibration across all classification tiers

### Phase 5: Optimization and Production Hardening (Weeks 9-10)
- **Performance Optimization**: Model compression, inference optimization, caching strategies
- **Monitoring and Alerting**: Comprehensive monitoring for model drift and performance degradation
- **Documentation**: Complete technical documentation and operational runbooks
- **Stakeholder Review**: Final review and approval from technical stakeholders

**Deliverables:**
- `docs/multiclass_operations_guide.md` - Operational procedures and troubleshooting
- `glyphsieve/ml/monitoring.py` - Model performance monitoring system
- `tests/ml/test_multiclass_integration.py` - Comprehensive integration test suite

**Success Criteria:**
- Production deployment with <1% error rate
- Complete monitoring and alerting coverage
- Stakeholder approval for full production rollout

## Feature Engineering Strategy

### Enhanced Text Features
1. **Advanced N-grams**: Extend beyond (1,2) to include (1,2,3) grams for better model discrimination
2. **Named Entity Recognition**: Extract manufacturer names, model numbers, and technical specifications
3. **Regex Pattern Features**: GPU-specific patterns for model numbers, memory sizes, and performance tiers
4. **Title Structure Analysis**: Position-based features for model information extraction

### Numerical Features
1. **Price Range Categorization**: Price bins corresponding to GPU performance tiers
2. **Memory Size Extraction**: VRAM size as a strong discriminative feature
3. **Performance Benchmarks**: Integration with external GPU benchmark databases
4. **Market Timing**: Release date and market age features for generation classification

### Categorical Features
1. **Seller Type Classification**: Professional vs consumer seller patterns
2. **Geographic Market Indicators**: Regional pricing and availability patterns
3. **Listing Category Analysis**: Product category and subcategory features
4. **Condition and Availability**: New vs used, stock status patterns

### External Data Integration
1. **GPU Specification Database**: Technical specifications from NVIDIA, AMD databases
2. **Market Data**: Historical pricing, performance benchmarks, release dates
3. **Manufacturer Information**: Official product lines, naming conventions, specifications
4. **Performance Metrics**: Gaming benchmarks, professional workload performance data

## Label Strategy Design

### Primary Label Hierarchy

#### Tier 1: GPU Family Classification
- **GeForce Consumer**: Gaming-focused consumer GPUs (RTX 4070, GTX 1650, etc.)
- **RTX Professional**: Workstation and professional GPUs (RTX A2000, RTX 6000 ADA, etc.)
- **Quadro Legacy**: Legacy professional GPU line (Quadro P2000, etc.)
- **Tesla/Data Center**: Server and data center GPUs (Tesla V100, A100, etc.)

#### Tier 2: Generation Classification
**GeForce Consumer:**
- RTX 50-series (RTX 5090, 5080, 5070, etc.)
- RTX 40-series (RTX 4090, 4080, 4070, etc.)
- RTX 30-series (RTX 3090, 3080, 3070, etc.)
- RTX 20-series (RTX 2080 Ti, 2070, etc.)
- GTX 16-series (GTX 1660, 1650, etc.)
- GTX 10-series (GTX 1080, 1070, etc.)

**RTX Professional:**
- RTX ADA Generation (RTX 6000 ADA, RTX 4000 SFF ADA, etc.)
- RTX Ampere Generation (RTX A6000, A5000, A4000, etc.)

#### Tier 3: Performance Classification
- **Flagship**: xx90 series (RTX 4090, 3090, etc.)
- **High-End**: xx80 series (RTX 4080, 3080, etc.)
- **Upper Mid-Range**: xx70 series (RTX 4070, 3070, etc.)
- **Mid-Range**: xx60 series (RTX 4060, 3060, etc.)
- **Entry-Level**: xx50 series (RTX 4050, 3050, etc.)
- **Professional**: Workstation and server GPUs

#### Tier 4: Specific Model Classification
Direct mapping to the 58 unique models identified in the dataset (RTX_4070, RTX_3060_TI, etc.)

### Label Sourcing and Quality Strategy

1. **Automated Label Generation**: Use existing `canonical_model` field as ground truth for specific models
2. **Rule-Based Family Assignment**: Implement rules to map specific models to families and generations
3. **Manual Validation**: Human review of edge cases and ambiguous classifications
4. **External Validation**: Cross-reference with official NVIDIA/AMD product databases
5. **Continuous Quality Monitoring**: Track label consistency and accuracy over time

### Handling Ambiguous Cases

1. **Mixed Listings**: Listings containing multiple GPU models → classify as "Mixed/Bundle"
2. **Incomplete Information**: Insufficient data for specific classification → fall back to higher tier
3. **New Models**: Unknown GPU models → classify using similarity to known models
4. **Conflicting Signals**: Multiple classification signals disagree → use confidence-weighted voting

## Risk Assessment and Mitigation Strategies

### Technical Risks

**Risk: Model Performance Degradation**
- *Probability*: Medium
- *Impact*: High
- *Mitigation*: Comprehensive A/B testing, gradual rollout, performance monitoring with automatic rollback

**Risk: Training Data Insufficiency**
- *Probability*: Medium
- *Impact*: Medium
- *Mitigation*: Data augmentation techniques, transfer learning from binary classifier, active learning for rare classes

**Risk: Feature Engineering Complexity**
- *Probability*: Low
- *Impact*: Medium
- *Mitigation*: Incremental feature addition, feature importance analysis, automated feature selection

**Risk: Integration Complexity**
- *Probability*: Medium
- *Impact*: High
- *Mitigation*: Staged integration approach, comprehensive testing, backward compatibility maintenance

### Business Risks

**Risk: Increased Operational Complexity**
- *Probability*: High
- *Impact*: Medium
- *Mitigation*: Comprehensive documentation, automated monitoring, operational runbooks

**Risk: Performance Impact on Existing Pipeline**
- *Probability*: Medium
- *Impact*: High
- *Mitigation*: Performance benchmarking, optimization strategies, caching mechanisms

**Risk: Label Quality Degradation**
- *Probability*: Medium
- *Impact*: High
- *Mitigation*: Automated quality checks, human validation processes, continuous monitoring

### Data Risks

**Risk: GPU Market Evolution**
- *Probability*: High
- *Impact*: Medium
- *Mitigation*: Regular model retraining, adaptive classification thresholds, new model detection

**Risk: Seller Behavior Changes**
- *Probability*: Medium
- *Impact*: Medium
- *Mitigation*: Feature robustness analysis, seller pattern monitoring, adaptive feature weighting

## Integration Strategy

### ml_signal.py Enhancement

The existing `ml_signal.py` module will be extended to support hierarchical predictions:

```python
@dataclass
class MulticlassGPUPrediction:
    is_gpu: bool
    gpu_confidence: float
    family: Optional[str] = None
    family_confidence: Optional[float] = None
    generation: Optional[str] = None
    generation_confidence: Optional[float] = None
    performance_tier: Optional[str] = None
    performance_confidence: Optional[float] = None
    specific_model: Optional[str] = None
    model_confidence: Optional[float] = None

def predict_gpu_multiclass(title: str, bulk_notes: str, price: Optional[float] = None) -> MulticlassGPUPrediction:
    """Enhanced prediction function supporting hierarchical GPU classification."""
    # Stage 1: Binary classification (existing)
    is_gpu, gpu_conf = predict_is_gpu(title, bulk_notes)
    
    if not is_gpu:
        return MulticlassGPUPrediction(is_gpu=False, gpu_confidence=gpu_conf)
    
    # Stage 2: Family classification
    family, family_conf = predict_gpu_family(title, bulk_notes, price)
    
    # Stage 3: Generation classification
    generation, gen_conf = predict_gpu_generation(title, bulk_notes, family)
    
    # Stage 4: Specific model classification
    model, model_conf = predict_specific_model(title, bulk_notes, family, generation)
    
    return MulticlassGPUPrediction(
        is_gpu=True,
        gpu_confidence=gpu_conf,
        family=family,
        family_confidence=family_conf,
        generation=generation,
        generation_confidence=gen_conf,
        specific_model=model,
        model_confidence=model_conf
    )
```

### Pipeline Integration Points

1. **Normalization Pipeline**: Add multiclass columns to output CSV
2. **Scoring System**: Incorporate GPU-specific performance characteristics
3. **API Endpoints**: Expose multiclass predictions through REST API
4. **Batch Processing**: Support multiclass predictions in backfill operations

### Backward Compatibility

- Existing binary classification functionality remains unchanged
- New multiclass features are additive and optional
- Existing API contracts are preserved
- Migration path provided for existing integrations

## Success Metrics and Evaluation Criteria

### Model Performance Metrics

**Stage 2 - Family Classification:**
- F1-score ≥ 0.90 across all GPU families
- Precision ≥ 0.88 for each family class
- Recall ≥ 0.88 for each family class
- Confusion matrix analysis with <5% cross-family misclassification

**Stage 3 - Generation Classification:**
- F1-score ≥ 0.85 per GPU family
- Temporal accuracy: <2% misclassification across adjacent generations
- Coverage: ≥95% of GPU samples successfully classified

**Stage 4 - Specific Model Classification:**
- F1-score ≥ 0.80 overall
- Top-3 accuracy ≥ 0.95 for specific model predictions
- Confidence calibration: predicted confidence correlates with actual accuracy

### System Performance Metrics

- **Latency**: End-to-end prediction latency <200ms
- **Throughput**: Support ≥1000 predictions per second
- **Memory Usage**: Total model memory footprint <500MB
- **Availability**: 99.9% uptime for prediction services

### Business Impact Metrics

- **Market Analysis Enhancement**: 50% improvement in GPU trend identification accuracy
- **Pricing Model Improvement**: 15% reduction in pricing prediction error
- **User Experience**: 25% improvement in search and filtering precision
- **Operational Efficiency**: <10% increase in overall system complexity

## Future Development Opportunities

### Short-term Enhancements (3-6 months)
1. **AMD GPU Support**: Extend classification to AMD Radeon GPU families
2. **Intel GPU Integration**: Add support for Intel Arc GPU classification
3. **Mobile GPU Classification**: Extend to laptop and mobile GPU variants
4. **Real-time Learning**: Implement online learning for new GPU model detection

### Medium-term Opportunities (6-12 months)
1. **Multi-modal Classification**: Incorporate image-based GPU identification
2. **Market Trend Prediction**: Use classification data for market forecasting
3. **Automated Pricing**: GPU-specific pricing models based on classification
4. **Competitive Analysis**: Cross-platform GPU market analysis

### Long-term Vision (12+ months)
1. **Universal Hardware Classification**: Extend beyond GPUs to CPUs, motherboards, etc.
2. **AI-Powered Market Intelligence**: Advanced analytics and trend prediction
3. **Dynamic Classification**: Self-adapting classification based on market changes
4. **Cross-language Support**: Multi-language GPU classification capabilities

## Alternatives Considered

### Alternative 1: Single-Stage Multiclass Classifier
**Approach**: Direct classification from text to specific GPU model
**Pros**: Simpler architecture, single model to maintain
**Cons**: Poor graceful degradation, difficult to debug, lower accuracy for rare classes
**Rejection Reason**: Lacks robustness and interpretability required for production system

### Alternative 2: Ensemble of Binary Classifiers
**Approach**: Multiple binary classifiers (one per GPU model) with voting
**Pros**: High accuracy for well-represented classes, easy to add new models
**Cons**: Exponential model growth, poor handling of new GPU models, high computational cost
**Rejection Reason**: Scalability concerns and maintenance complexity

### Alternative 3: Deep Learning Transformer Approach
**Approach**: Fine-tuned BERT/RoBERTa for GPU classification
**Pros**: State-of-the-art text classification performance, handles complex patterns
**Cons**: High computational requirements, difficult to interpret, requires large datasets
**Rejection Reason**: Computational overhead incompatible with current infrastructure constraints

### Alternative 4: Rule-Based Enhancement
**Approach**: Extend existing regex/fuzzy matching with more sophisticated rules
**Pros**: Interpretable, fast, easy to maintain
**Cons**: Limited scalability, requires manual rule creation, poor generalization
**Rejection Reason**: Cannot handle the complexity and variety of multiclass requirements

## Conclusion

The hierarchical multiclass GPU categorizer represents a natural evolution of the current binary classification system. By building upon the proven foundation of perfect binary classification performance, this approach provides a robust, scalable path to granular GPU categorization while maintaining system reliability and performance.

The staged implementation plan allows for incremental validation and rollout, minimizing risk while maximizing business value. The comprehensive feature engineering strategy and label hierarchy design ensure the system can handle the complexity of modern GPU markets while remaining maintainable and extensible.

Success of this initiative will position the GPU Scoring Tool as the industry leader in automated GPU market analysis, providing unprecedented insights into GPU pricing, availability, and market trends.

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-31  
**Next Review**: 2025-08-31  
**Stakeholders**: ML Engineering Team, Product Management, Data Science Team