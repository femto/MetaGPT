#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/1 22:50
@Author  : alexanderwu
@File    : test_azure_tts.py
@Modified By: mashenquan, 2023-8-9, add more text formatting options
@Modified By: mashenquan, 2023-8-17, move to `tools` folder.
"""

import pytest
from azure.cognitiveservices.speech import ResultReason

from metagpt.config import CONFIG
from metagpt.config2 import config
from metagpt.tools.azure_tts import AzureTTS


@pytest.mark.asyncio
async def test_azure_tts():
    # Prerequisites
    assert CONFIG.AZURE_TTS_SUBSCRIPTION_KEY and CONFIG.AZURE_TTS_SUBSCRIPTION_KEY != "YOUR_API_KEY"
    assert CONFIG.AZURE_TTS_REGION

    azure_tts = AzureTTS(subscription_key="", region="")
    text = """
        女儿看见父亲走了进来，问道：
            <mstts:express-as role="YoungAdultFemale" style="calm">
                “您来的挺快的，怎么过来的？”
            </mstts:express-as>
            父亲放下手提包，说：
            <mstts:express-as role="OlderAdultMale" style="calm">
                “Writing a binary file in Python is similar to writing a regular text file, but you'll work with bytes instead of strings.”
            </mstts:express-as>
        """
    path = config.workspace.path / "tts"
    path.mkdir(exist_ok=True, parents=True)
    filename = path / "girl.wav"
    filename.unlink(missing_ok=True)
    result = await azure_tts.synthesize_speech(
        lang="zh-CN", voice="zh-CN-XiaomoNeural", text=text, output_file=str(filename)
    )
    print(result)
    assert result
    assert result.audio_data
    assert result.reason == ResultReason.SynthesizingAudioCompleted
    assert filename.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
