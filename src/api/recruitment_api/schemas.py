from pydantic import BaseModel, ConfigDict, Field

class Observations(BaseModel):
    id: int
    user_id: int
    center_freq_mhz: float = Field(min_value=1400.0, max_value=1440.0)
    status: str
    fits_file_url: str

    created_at: str
    started_at: str
    completed_at: str

    '''
    def observation_frequency(freq):
        if freq <1400.0 or freq>1440.0:
            raise ValueError(f"out of range frequency! {freq}"  )
        return freq
    '''