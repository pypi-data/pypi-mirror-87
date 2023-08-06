from duckietown_build_utils import repo_info_from_url
from . import logger


def test_repo_info():
    urls0 = urls.replace(" ", "")
    urls1 = urls0.split("\n")
    for u in urls1:
        u = u.strip()
        if not u:
            continue
        f = repo_info_from_url(u)
        logger.info(u=u, rep_info=f)


urls = """

git@github.com:duckietown/challenge-aido_LF-baseline-behavior-cloning.git


git@github.com:duckietown/dt-env-developer.git


git@github.com:duckietown/aido-robotarium-evaluation-form.git


git@github.com:duckietown/autolab_control_flask_scripts.git


git@github.com:duckietown/challenge-aido_LF-baseline-IL-logs-tensorflow.git


git@github.com:duckietown/challenge-aido_LF-baseline-JBR.git


git@github.com:duckietown/challenge-aido_LF-baseline-duckietown.git


git@github.com:duckietown/challenge-aido_LF-experiment_manager.git


git@github.com:duckietown/ETHZ-autolab-fleet-roster.git


git@github.com:duckietown/challenge-aido_LF.git


git@github.com:duckietown/challenge-aido_LF-baseline-RL-sim-pytorch.git


git@github.com:duckietown/aido-submission-ci-test.git


git@github.com:duckietown/challenge-aido_LF-duckiebot-bridge.git


git@github.com:duckietown/challenge-aido_LF-baseline-IL-sim-tensorflow.git





git@github.com:duckietown/challenge-aido_LF-minimal-agent.git


git@github.com:duckietown/challenge-aido_LF-scenario_maker.git


git@github.com:duckietown/challenge-aido_LF-minimal-agent-full.git


git@github.com:duckietown/challenge-aido_LF-template-pytorch.git


git@github.com:duckietown/challenge-aido_LF-template-ros.git


git@github.com:duckietown/challenge-multistep.git


git@github.com:duckietown/compose-pkg-lab_controls.git


git@github.com:duckietown/challenge-aido_LF-simulator-gym.git


git@github.com:duckietown/challenge-aido_LF-template-tensorflow.git


git@github.com:duckietown/planning-exercise-solution.git


git@github.com:duckietown/challenge-aido_LF-template-random.git


git@github.com:duckietown/planning-exercises.git



git@github.com:duckietown/challenge-prediction.git



git@github.com:duckietown/course-extra.git




git@github.com:duckietown/docs-AIDO.git


git@github.com:duckietown/docs-build.git


git@github.com:duckietown/docs-duckiesky_high_school.git


git@github.com:duckietown/docs-duckiesky_high_school_student.git


git@github.com:duckietown/docs-opmanual_autolab.git


git@github.com:duckietown/docs-duckumentation.git


git@github.com:duckietown/docs-opmanual_developer.git


git@github.com:duckietown/docs-opmanual_duckietown.git


git@github.com:duckietown/docs-opmanual_duckiebot.git


git@github.com:duckietown/duckuments-presentation-config.git


git@github.com:duckietown/docs-opmanual_sky.git


git@github.com:duckietown/mooc-notes.git


git@github.com:duckietown/docs-exercises.git


git@github.com:duckietown/docs-learning_materials.git


git@github.com:duckietown/docs-preliminaries.git


git@github.com:duckietown/docs-software_architecture.git


git@github.com:duckietown/docs-software_devel.git


git@github.com:duckietown/docs-software_reference.git


git@github.com:duckietown/aido-agents.git


git@github.com:duckietown/Software.git


git@github.com:duckietown/aido-base-python3.git


git@github.com:duckietown/aido-analyze.git


git@github.com:duckietown/aido-protocols.git


git@github.com:duckietown/docs-sphinxapi.git


git@github.com:duckietown/dt-base-environment.git


git@github.com:duckietown/dt-car-interface.git


git@github.com:duckietown/dt-commons.git


git@github.com:duckietown/dt-core.git


git@github.com:duckietown/dt-duckiebot-interface.git


git@github.com:duckietown/dt-duckiebot-fifos-bridge.git


git@github.com:duckietown/dt-ros-commons.git


git://github.com/duckietown/duckiebot-interface.git


git@github.com:duckietown/challenge-aido_lf-ros-bridge.git


git@github.com:duckietown/aido-utils.git


git@github.com:duckietown/duckietown-challenges.git


git@github.com:duckietown/duckietown-challenges-cli.git


git@github.com:duckietown/duckietown-challenges-runner.git


git@github.com:duckietown/duckietown-challenges-server.git


git@github.com:duckietown/duckietown-docker-utils.git


git@github.com:duckietown/duckietown-serialization.git


git@github.com:duckietown/duckietown-shell.git


git@github.com:duckietown/duckietown-shell-commands.git


git@github.com:duckietown/duckietown-sim-server.git


git@github.com:duckietown/duckietown-tokens.git


git@github.com:duckietown/duckietown-unity.git


git@github.com:duckietown/duckietown-utils.git


git@github.com:duckietown/duckietown-world.git


git@github.com:duckietown/gym-duckietown.git


git@github.com:duckietown/gym-duckietown-agent.git


git@github.com:duckietown/gym-duckietown-ros-agent.git


git@github.com:duckietown/gym-gazebo.git


git@github.com:duckietown/lib-dt-authentication.git


git@github.com:duckietown/lib-dt-data-api.git


git@github.com:duckietown/mooc-exercises.git


git@github.com:duckietown/mooc-fifos-connector.git


git@github.com:duckietown/sim-duckiebot-lanefollowing-demo.git


git@github.com:duckietown/duckietown-project-template.git


git@github.com:duckietown/template-basic.git


git@github.com:duckietown/template-compose.git


git@github.com:duckietown/template-library.git


git@github.com:duckietown/template-docs.git


git@github.com:duckietown/template-ros.git


git@github.com:duckietown/template-ros-core.git


https://github.com/duckietown/challenge-aido_LF-baseline-behavior-cloning.git


https://github.com/duckietown/dt-env-developer.git


https://github.com/duckietown/aido-robotarium-evaluation-form.git


https://github.com/duckietown/autolab_control_flask_scripts.git


https://github.com/duckietown/challenge-aido_LF-baseline-IL-logs-tensorflow.git


https://github.com/duckietown/challenge-aido_LF-baseline-JBR.git


https://github.com/duckietown/challenge-aido_LF-baseline-duckietown.git


https://github.com/duckietown/challenge-aido_LF-experiment_manager.git


https://github.com/duckietown/ETHZ-autolab-fleet-roster.git


https://github.com/duckietown/challenge-aido_LF.git


https://github.com/duckietown/challenge-aido_LF-baseline-RL-sim-pytorch.git


https://github.com/duckietown/aido-submission-ci-test.git


https://github.com/duckietown/challenge-aido_LF-duckiebot-bridge.git


https://github.com/duckietown/challenge-aido_LF-baseline-IL-sim-tensorflow.git





https://github.com/duckietown/challenge-aido_LF-minimal-agent.git


https://github.com/duckietown/challenge-aido_LF-scenario_maker.git


https://github.com/duckietown/challenge-aido_LF-minimal-agent-full.git


https://github.com/duckietown/challenge-aido_LF-template-pytorch.git


https://github.com/duckietown/challenge-aido_LF-template-ros.git


https://github.com/duckietown/challenge-multistep.git


https://github.com/duckietown/compose-pkg-lab_controls.git


https://github.com/duckietown/challenge-aido_LF-simulator-gym.git


https://github.com/duckietown/challenge-aido_LF-template-tensorflow.git


https://github.com/duckietown/planning-exercise-solution.git


https://github.com/duckietown/challenge-aido_LF-template-random.git


https://github.com/duckietown/planning-exercises.git



https://github.com/duckietown/challenge-prediction.git



https://github.com/duckietown/course-extra.git




https://github.com/duckietown/docs-AIDO.git


https://github.com/duckietown/docs-build.git


https://github.com/duckietown/docs-duckiesky_high_school.git


https://github.com/duckietown/docs-duckiesky_high_school_student.git


https://github.com/duckietown/docs-opmanual_autolab.git


https://github.com/duckietown/docs-duckumentation.git


https://github.com/duckietown/docs-opmanual_developer.git


https://github.com/duckietown/docs-opmanual_duckietown.git


https://github.com/duckietown/docs-opmanual_duckiebot.git


https://github.com/duckietown/duckuments-presentation-config.git


https://github.com/duckietown/docs-opmanual_sky.git


https://github.com/duckietown/mooc-notes.git


https://github.com/duckietown/docs-exercises.git


https://github.com/duckietown/docs-learning_materials.git


https://github.com/duckietown/docs-preliminaries.git


https://github.com/duckietown/docs-software_architecture.git


https://github.com/duckietown/docs-software_devel.git


https://github.com/duckietown/docs-software_reference.git


https://github.com/duckietown/aido-agents.git


https://github.com/duckietown/Software.git


https://github.com/duckietown/aido-base-python3.git


https://github.com/duckietown/aido-analyze.git


https://github.com/duckietown/aido-protocols.git


https://github.com/duckietown/docs-sphinxapi.git


https://github.com/duckietown/dt-base-environment.git


https://github.com/duckietown/dt-car-interface.git


https://github.com/duckietown/dt-commons.git


https://github.com/duckietown/dt-core.git


https://github.com/duckietown/dt-duckiebot-interface.git


https://github.com/duckietown/dt-duckiebot-fifos-bridge.git


https://github.com/duckietown/dt-ros-commons.git


git://github.com/duckietown/duckiebot-interface.git


https://github.com/duckietown/challenge-aido_lf-ros-bridge.git


https://github.com/duckietown/aido-utils.git


https://github.com/duckietown/duckietown-challenges.git


https://github.com/duckietown/duckietown-challenges-cli.git


https://github.com/duckietown/duckietown-challenges-runner.git


https://github.com/duckietown/duckietown-challenges-server.git


https://github.com/duckietown/duckietown-docker-utils.git


https://github.com/duckietown/duckietown-serialization.git


https://github.com/duckietown/duckietown-shell.git


https://github.com/duckietown/duckietown-shell-commands.git


https://github.com/duckietown/duckietown-sim-server.git


https://github.com/duckietown/duckietown-tokens.git


https://github.com/duckietown/duckietown-unity.git


https://github.com/duckietown/duckietown-utils.git


https://github.com/duckietown/duckietown-world.git


https://github.com/duckietown/gym-duckietown.git


https://github.com/duckietown/gym-duckietown-agent.git


https://github.com/duckietown/gym-duckietown-ros-agent.git


https://github.com/duckietown/gym-gazebo.git


https://github.com/duckietown/lib-dt-authentication.git


https://github.com/duckietown/lib-dt-data-api.git


https://github.com/duckietown/mooc-exercises.git


https://github.com/duckietown/mooc-fifos-connector.git


https://github.com/duckietown/sim-duckiebot-lanefollowing-demo.git


https://github.com/duckietown/duckietown-project-template.git


https://github.com/duckietown/template-basic.git


https://github.com/duckietown/template-compose.git


https://github.com/duckietown/template-library.git


https://github.com/duckietown/template-docs.git


https://github.com/duckietown/template-ros.git


https://github.com/duckietown/template-ros-core.git





"""
