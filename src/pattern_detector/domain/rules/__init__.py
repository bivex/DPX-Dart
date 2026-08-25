from typing import List
from .base import Rule
from .idiomatic_rules import (
    SealedClassAdtRule,
    PatternMatchingSwitchRule,
    RecordMultipleReturnRule,
    ExtensionTypeInlinedRule,
    EnhancedEnumMembersRule,
    MixinBehaviorCompositionRule,
    ExtensionMethodSugarRule,
)
from .flutter_rules import (
    BlocCubitStateMachineRule,
    RiverpodNotifierDiRule,
    InheritedWidgetProviderRule,
    ChangeNotifierStoreRule,
    CleanUsecaseInteractorRule,
)
from .concurrency_rules import (
    IsolateWorkerPoolRule,
    AsyncStreamPipelineRule,
)
from .creational_rules import (
    FactoryConstructorRule,
    BuilderWidgetPatternRule,
    PrototypeCopyWithRule,
    SingletonInstanceRule,
    ServiceLocatorDiRule,
)
from .structural_rules import (
    AdapterTypeConverterRule,
    BridgePlatformChannelRule,
    CompositeWidgetTreeRule,
    DecoratorWrapperWidgetRule,
    FacadeApiClientRule,
    FlyweightConstInstanceRule,
    ProxyCachedRepositoryRule,
)
from .behavioral_rules import (
    ChainMiddlewareInterceptorRule,
    CommandIntentActionRule,
    IteratorSyncGeneratorRule,
    MediatorEventBusRule,
    MementoHydratedSnapshotRule,
    ObserverListenableStreamRule,
    StateMachineHierarchyRule,
    StrategyAlgorithmInterfaceRule,
    TemplateMethodLifecycleRule,
    VisitorWidgetTraversalRule,
)
from .security_rules import (
    AsyncGapContextUseHazardRule,
    UnclosedStreamControllerHazardRule,
    HardcodedApiKeySecretHazardRule,
    UnsafeEvalJsInjectionHazardRule,
    SetstateDuringBuildHazardRule,
    LateInitializationRaceHazardRule,
)
from .solid_principles_rules import (
    MonolithicWidgetSrpRule,
    GodClassServiceSrpRule,
    FatAbstractInterfaceIspRule,
)


def get_default_rules() -> List[Rule]:
    return [
        # Modern Idiomatic
        SealedClassAdtRule(),
        PatternMatchingSwitchRule(),
        RecordMultipleReturnRule(),
        ExtensionTypeInlinedRule(),
        EnhancedEnumMembersRule(),
        MixinBehaviorCompositionRule(),
        ExtensionMethodSugarRule(),
        # Flutter & Reactive
        BlocCubitStateMachineRule(),
        RiverpodNotifierDiRule(),
        InheritedWidgetProviderRule(),
        ChangeNotifierStoreRule(),
        CleanUsecaseInteractorRule(),
        # Concurrency & Async
        IsolateWorkerPoolRule(),
        AsyncStreamPipelineRule(),
        # Creational
        FactoryConstructorRule(),
        BuilderWidgetPatternRule(),
        PrototypeCopyWithRule(),
        SingletonInstanceRule(),
        ServiceLocatorDiRule(),
        # Structural
        AdapterTypeConverterRule(),
        BridgePlatformChannelRule(),
        CompositeWidgetTreeRule(),
        DecoratorWrapperWidgetRule(),
        FacadeApiClientRule(),
        FlyweightConstInstanceRule(),
        ProxyCachedRepositoryRule(),
        # Behavioral
        ChainMiddlewareInterceptorRule(),
        CommandIntentActionRule(),
        IteratorSyncGeneratorRule(),
        MediatorEventBusRule(),
        MementoHydratedSnapshotRule(),
        ObserverListenableStreamRule(),
        StateMachineHierarchyRule(),
        StrategyAlgorithmInterfaceRule(),
        TemplateMethodLifecycleRule(),
        VisitorWidgetTraversalRule(),
        # Security & Memory Hazards
        AsyncGapContextUseHazardRule(),
        UnclosedStreamControllerHazardRule(),
        HardcodedApiKeySecretHazardRule(),
        UnsafeEvalJsInjectionHazardRule(),
        SetstateDuringBuildHazardRule(),
        LateInitializationRaceHazardRule(),
        # SOLID
        MonolithicWidgetSrpRule(),
        GodClassServiceSrpRule(),
        FatAbstractInterfaceIspRule(),
    ]
