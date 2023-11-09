"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any, Union

from bluuberrylibrary.classes.bb_enqueue_interaction_result import BBEnqueueInteractionResult
from bluuberrylibrary.classes.bb_execute_interaction_result import BBExecuteInteractionResult
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.instances.bb_interaction_utils import BBInteractionUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from interactions.aop import AffordanceObjectPair
from interactions.base.interaction import Interaction
from interactions.base.mixer_interaction import MixerInteraction
from interactions.base.super_interaction import SuperInteraction
from interactions.context import InteractionContext, InteractionSource, QueueInsertStrategy
from interactions.priority import Priority
from interactions.social.social_mixer_interaction import SocialMixerInteraction
from interactions.social.social_super_interaction import SocialSuperInteraction
from sims.sim_info import SimInfo


class BBSimInteractionUtils:
    """Utilities for manipulating interactions on Sims."""

    @classmethod
    def create_interaction_context(
        cls,
        sim_info: SimInfo,
        interaction_source: InteractionSource = InteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT,
        priority: Priority = Priority.High,
        run_priority: Union[Priority, None] = Priority.High,
        insert_strategy: QueueInsertStrategy = QueueInsertStrategy.NEXT,
        must_run_next: bool = False,
        **kwargs
    ) -> Union[InteractionContext, None]:
        sim = BBSimUtils.to_sim_instance(sim_info)
        if sim is None:
            return
        return InteractionContext(
            sim,
            interaction_source,
            priority,
            run_priority=run_priority,
            insert_strategy=insert_strategy,
            must_run_next=must_run_next,
            **kwargs
        )

    @classmethod
    def push_interaction(
        cls,
        mod_identity: BBModIdentity,
        sim_info: SimInfo,
        interaction: int,
        social_super_interaction: int = None,
        target: Any = None,
        picked_object: Any = None,
        interaction_context: InteractionContext = None,
        **kwargs
    ) -> BBEnqueueInteractionResult:
        sim = BBSimUtils.to_sim_instance(sim_info)
        if sim is None:
            raise AssertionError('Attempted to push an interaction onto a Sim that is not loaded.')
        if sim.si_state is None:
            return BBEnqueueInteractionResult(BBTestResult(False, reason=f'Sim {sim_info} did not have a Super Interaction State.'), BBExecuteInteractionResult.NONE)
        if sim.queue is None:
            return BBEnqueueInteractionResult(BBTestResult(False, reason=f'Sim {sim_info} did not have a Queue.'), BBExecuteInteractionResult.NONE)
        # noinspection PyPropertyAccess
        if sim.posture_state is None:
            return BBEnqueueInteractionResult(BBTestResult(False, reason=f'Sim {sim_info} did not have a Posture State.'), BBExecuteInteractionResult.NONE)
        if sim.posture is None:
            return BBEnqueueInteractionResult(BBTestResult(False, reason=f'Sim {sim_info} did not have a Posture.'), BBExecuteInteractionResult.NONE)

        interaction_instance: Interaction = BBInteractionUtils.load_interaction_by_guid(interaction)
        if interaction_instance is None:
            return BBEnqueueInteractionResult(BBTestResult(False, reason=f'Interaction did not exist with id {interaction}'), BBExecuteInteractionResult.NONE)

        if social_super_interaction is not None:
            # noinspection PyTypeChecker
            social_super_interaction_instance: SocialSuperInteraction = BBInteractionUtils.load_interaction_by_guid(social_super_interaction)
        else:
            # noinspection PyTypeChecker
            social_super_interaction_instance: SocialSuperInteraction = None

        interaction_context = interaction_context or cls.create_interaction_context(
            sim_info,
            insert_strategy=QueueInsertStrategy.LAST
        )

        if BBInteractionUtils.is_super_interaction(interaction_instance):
            # noinspection PyTypeChecker
            interaction_instance: SuperInteraction = interaction_instance
            return cls._push_super_interaction(
                mod_identity,
                sim_info,
                interaction_instance,
                target=target,
                picked_object=picked_object,
                interaction_context=interaction_context,
                **kwargs
            )

        if BBInteractionUtils.is_social_mixer_interaction(interaction_instance):
            # noinspection PyTypeChecker
            interaction_instance: SocialMixerInteraction = interaction_instance
            return cls._push_social_mixer_interaction(
                mod_identity,
                sim_info,
                target,
                interaction_instance,
                social_super_interaction_instance,
                picked_object,
                interaction_context,
                **kwargs
            )

        # noinspection PyTypeChecker
        interaction_instance: MixerInteraction = interaction_instance
        return cls._push_mixer_interaction(
            mod_identity,
            sim_info,
            interaction_instance,
            target,
            interaction_context
        )

    @classmethod
    def _push_super_interaction(
        cls,
        mod_identity: BBModIdentity,
        sim_info: SimInfo,
        super_interaction: SuperInteraction,
        target: Any,
        picked_object: Any,
        interaction_context: InteractionContext,
        **kwargs
    ) -> BBEnqueueInteractionResult:

        if target is not None and isinstance(target, SimInfo):
            target = BBSimUtils.to_sim_instance(target)

        interaction_context = interaction_context or cls.create_interaction_context(sim_info)

        sim = BBSimUtils.to_sim_instance(sim_info)
        result = sim.push_super_affordance(
            super_interaction,
            target,
            interaction_context,
            picked_object=picked_object or target,
            **kwargs
        )
        return BBEnqueueInteractionResult.from_base(result)

    @classmethod
    def _push_social_mixer_interaction(
        cls,
        mod_identity: BBModIdentity,
        sim_info: SimInfo,
        target: SimInfo,
        social_mixer_interaction: SocialMixerInteraction,
        social_super_interaction: SocialSuperInteraction,
        picked_object: Any,
        interaction_context: InteractionContext,
        **kwargs
    ):
        sim = BBSimUtils.to_sim_instance(sim_info)

        interaction_context = interaction_context or cls.create_interaction_context(sim_info)

        if social_super_interaction is not None:
            target_sim = BBSimUtils.to_sim_instance(target)

            def _get_existing_interaction(si_iter) -> Interaction:
                for si in si_iter:
                    if si.super_affordance != social_super_interaction:
                        continue
                    if si.social_group is None:
                        continue
                    if target_sim is not None and target_sim not in si.social_group:
                        continue
                    return si.super_interaction

            super_interaction = _get_existing_interaction(sim.si_state) or _get_existing_interaction(sim.queue)
            if super_interaction is None:
                si_result = cls._push_super_interaction(
                    mod_identity,
                    sim_info,
                    social_super_interaction,
                    target,
                    picked_object,
                    interaction_context,
                    **kwargs
                )
                if not si_result:
                    return BBEnqueueInteractionResult(BBTestResult.TRUE, BBExecuteInteractionResult(False, None, 'No Super Interaction was found.'))
                super_interaction = si_result.execute_result.interaction

            pick = interaction_context.pick if interaction_context.pick is not None else super_interaction.context.pick
            interaction_context = super_interaction.context.clone_for_continuation(
                super_interaction,
                insert_strategy=interaction_context.insert_strategy,
                source_interaction_id=super_interaction.id,
                source_interaction_sim_id=BBSimUtils.to_sim_id(sim_info),
                pick=pick,
                picked_object=picked_object,
                must_run_next=interaction_context.must_run_next,
                **kwargs
            )
        else:
            super_interaction = None

        aop = AffordanceObjectPair(
            social_mixer_interaction,
            target,
            social_super_interaction,
            super_interaction,
            picked_object=picked_object or target,
            push_super_on_prepare=True,
            **kwargs
        )
        result = aop.test_and_execute(interaction_context)
        return BBEnqueueInteractionResult.from_base(result)

    @classmethod
    def _push_mixer_interaction(
        cls,
        mod_identity: BBModIdentity,
        sim_info: SimInfo,
        mixer_interaction: MixerInteraction,
        target: Any,
        interaction_context: InteractionContext,
        **kwargs
    ):
        from autonomy.content_sets import get_valid_aops_gen

        sim = BBSimUtils.to_sim_instance(sim_info)
        if target is not None and isinstance(target, SimInfo):
            target = BBSimUtils.to_sim_instance(target)

        source_interaction = sim.posture.source_interaction
        if source_interaction is None:
            return BBEnqueueInteractionResult(BBTestResult.TRUE, BBExecuteInteractionResult(False, None, f'No source interaction found on Sim {sim_info}'))

        if hasattr(mixer_interaction, 'lock_out_time') and mixer_interaction.lock_out_time:
            sim_specific_lockout = mixer_interaction.lock_out_time.target_based_lock_out
        else:
            sim_specific_lockout = False

        if sim_specific_lockout and sim.is_sub_action_locked_out(mixer_interaction):
            return BBEnqueueInteractionResult(BBTestResult(False, reason=f'{sim_info} is currently locked out of doing the mixer interaction, they must wait before they can do it again.'), BBExecuteInteractionResult.NONE)

        super_interaction_instance = source_interaction.super_affordance
        interaction_context = interaction_context or cls.create_interaction_context(sim_info)
        for (aop, test_result) in get_valid_aops_gen(
            target,
            mixer_interaction,
            super_interaction_instance,
            source_interaction,
            interaction_context,
            False,
            push_super_on_prepare=False
        ):
            test_result: BBTestResult = BBTestResult.from_base(test_result)
            if test_result is None or test_result.result:
                continue
            interaction_constraint = aop.constraint_intersection(sim=sim, posture_state=None)
            # noinspection PyPropertyAccess
            posture_constraint = sim.posture_state.posture_constraint_strict
            constraint_intersection = interaction_constraint.intersect(posture_constraint)
            if not constraint_intersection.valid:
                continue
            return BBEnqueueInteractionResult.from_base(aop.execute(interaction_context, **kwargs))
