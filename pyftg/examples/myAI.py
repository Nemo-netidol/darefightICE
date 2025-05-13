from pyftg import (AIInterface, GameData, CommandCenter, FrameData, Key, RoundResult, ScreenData, AudioData)
import logging
import librosa
import csv
import numpy as np
import os

logger = logging.getLogger(__name__)
class myAI(AIInterface):
    def __init__(self):
        super().__init__()
        self.blind_flag = False
        self.audio_log = []
        self.frame_count = 0
        self.output_dir = 'audio_dataset'

    def name(self) -> str:
        return self.__class__.__name__

    def is_blind(self) -> bool:
        return self.blind_flag

    def initialize(self, game_data: GameData, player_number: int):
        logger.info("initialize myAI")
        self.cc = CommandCenter()
        self.key = Key()
        self.player = player_number

    def input(self) -> Key:
        return self.key

    def get_information(self, frame_data: FrameData, is_control: bool):
        self.frame_data = frame_data
        self.cc.set_frame_data(frame_data, self.player)

    def processing(self):
        if self.frame_data.empty_flag or self.frame_data.current_frame_number <= 0:
            return

        if self.cc.get_skill_flag():
            self.key = self.cc.get_skill_key()
        else:
            self.key.empty()
            self.cc.skill_cancel()

            self.cc.command_call("A")
        
    def get_screen_data(self, screen_data: ScreenData):
        self.screen_data = screen_data

    def get_audio_data(self, audio_data: AudioData):
        self.audio_data = audio_data
        
        data = np.frombuffer(audio_data.raw_data_bytes)

        mfcc = librosa.feature.mfcc(y=data, n_mfcc=13)

        mfcc_vector = mfcc.mean(axis=1)

        self.audio_log.append([self.frame_count] + mfcc_vector.tolist())
        self.frame_count += 1

        # print("audio data: ", self.audio_data)
    
    def get_non_delay_frame_data(self, frame_data: FrameData):
        pass
    
    def round_end(self, round_result: RoundResult):
        logger.info(f"round end: {round_result}")

    def game_end(self):
        csv_file = os.path.join(self.output_dir, "audio_data.csv")
        with open(csv_file, "w") as file:
            writer = csv.writer(file)

            writer.writerow(["frame"] + [f"mfcc_{i}" for i in range(13)])

            writer.writerows(self.audio_log)

            print(f"Saved audio data to {csv_file}")

        logger.info("game end")
    
    def close(self):
        pass
        
             
