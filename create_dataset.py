import os
import numpy as np
import pandas as pd
import librosa
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

folder_path = r'C:\Users\ALEXIS\Documents\Sinclair\Spring Semester\2266_python\Honors project\Selected_songs'

# ======= SONGS WITH THEIR EMOTION =======
file_to_emotion = {
    'ACDC - Thunderstruck.mp3': 'Energetic',
    'Bad Boys Theme.mp3': 'Energetic',
    'Bobby McFerrin - Don\'t Worry Be Happy.mp3': 'Happy',
    'Bruno Mars - Just the way you are.mp3': 'Romantic',
    'Can\'t Hold Us - Macklemore & Ryan Lewis.mp3': 'Energetic',
    'Disturbed - The Sound Of Silence.mp3': 'Sad',
    'Ed Sheeran - Thinking Out Loud.mp3': 'Romantic',
    'Evanescence - My Immortal.mp3': 'Sad',
    'Gary Jules - Mad World.mp3': 'Sad',
    'Hozier - Take Me To Church.mp3': 'Sad',
    'Jack Johnson - Better Together.mp3': 'Calm',
    'John Mayer - Slow Dancing In A Burning Room.mp3': 'Calm',
    'Katrina And The Waves - Walking On Sunshine.mp3': 'Happy',
    'Lewis Capaldi - Someone You Loved.mp3': 'Sad',
    'Lizzo - Good As Hell.mp3': 'Happy',
    'Nirvana - Smells Like Teen Spirit.mp3': 'Angry',
    'Post Malone - Sunflower.mp3': 'Happy',
    'Radiohead - Karma Police.mp3': 'Sad',
    'Sia - Chandelier.mp3': 'Sad',
    'Survivor - Eye of the Tiger.mp3': 'Energetic',
    'The Beatles - Blackbird.mp3': 'Calm',
    'Tom Odell - Another Love.mp3': 'Sad',
    'Adele - Skyfall.mp3': 'Calm',
    'Billie Eilish - everything i wanted.mp3': 'Sad',
    'Bon Iver - Holocene.mp3': 'Calm',
    'Bruno Mars - Uptown funk.mp3': 'Happy',
    'Coldplay - Fix You.mp3': 'Sad',
    'Drowning pool - Bodies.mp3': 'Angry',
    'Elvis Presley - Can\'t Help Falling In Love.mp3': 'Romantic',
    'Fleetwood Mac - Landslide.mp3': 'Calm',
    'Green Day - American Idiot.mp3': 'Angry',
    'Imagine Dragons - Believer.mp3': 'Energetic',
    'James Arthur - Say You Won\'t cwGo.mp3': 'Romantic',
    'Johnny Cash - Hurt.mp3': 'Sad',
    'Katy Perry - Firework.mp3': 'Happy',
    'Limp Bizkit - Break Stuff.mp3': 'Angry',
    'LMFAO - Party Rock Anthem.mp3': 'Happy',
    'Norah Jones - Come Away With Me.mp3': 'Calm',
    'Queen - Don\'t Stop Me Now.mp3': 'Energetic',
    'Rage against the Machine - Killing in the Name.mp3': 'Angry',
    'Skinny Love.mp3': 'Sad',
    'Slipknot - Duality.mp3': 'Angry',
    'Solo Leveling Opening.mp3': 'Energetic',
    'Taylor Swift - Shake It Off.mp3': 'Happy',
    'The Temptations - My Girl.mp3': 'Romantic',
    'Three Days Grace - Animal I Have Become.mp3': 'Angry',
    'Fleetwood Mac - Dreams.mp3': 'Calm',
    'Harry Styles - Adore You.mp3': 'Romantic',
    'Michael Bublé - Everything.mp3': 'Romantic',
    'Imagine Dragons - Demons.mp3': 'Sad',
    'Eric Clapton - Tears In Heaven.mp3': 'Sad',
    'Linkin Park - Given Up.mp3': 'Angry',
    'Yiruma - River Flows in You.mp3': 'Calm',
    'Sia - Breathe Me.mp3': 'Sad',
    'You Can\'t Take Me - Spirit the movie.mp3': 'Energetic',
    'Linkin Park - In the End.mp3': 'Sad',
    'Frank Sinatra - Fly me to the moon.mp3': 'Romantic',
    'Pharrel Williams - Happy.mp3': 'Happy',
    'Israel Kamakawiwo\'ole - Somewhere Over the Rainbow.mp3': 'Calm',
    'Ed Sheeran - Tenerife Sea.mp3': 'Calm',
    'Hans Zimmer - Time.mp3': 'Calm',
    'Jeff Buckley - Hallelujah.mp3': 'Calm',
    'Kanye West - Stronger.mp3': 'Energetic',
    'R.E.M. - Everybody Hurts.mp3': 'Sad',
    'Scorpions - Rock You Like a Hurricane.mp3': 'Energetic',
    'System Of A Down - Chop Suey.mp3': 'Angry',

    'Papa Roach - Last Resort.mp3': 'Angry',
    'Limp Bizkit - Freak On a Leash.mp3': 'Angry',
    'Nine Inch Nails - Head Like A Hole.mp3': 'Angry',
    'Metallica - Enter Sandman.mp3': 'Angry',
    'System of a Down - Toxicity.mp3': 'Angry',
    'Pantera - Walk.mp3': 'Angry',
    'Linkin Park - One Step Closer.mp3': 'Angry',
    'Eminem - The Way I Am.mp3': 'Angry',
    'Rage Against The Machine - Bulls On Parade.mp3': 'Angry',
    'Limp Bizkit - Rollin\'.mp3': 'Angry',

    'Jack Johnson - Banana Pancakes.mp3': 'Calm',
    'Vance Joy - Riptide.mp3': 'Calm',
    'Norah Jones - Sunrise.mp3': 'Calm',
    'James Blunt - You\'re Beautiful.mp3': 'Calm',
    'Ed Sheeran - Photograph.mp3': 'Calm',
    'John Mayer - Gravity.mp3': 'Calm',
    'Louis Armstrong - What a Wonderful World.mp3': 'Calm',
    'Coldplay - Yellow.mp3': 'Calm',
    'The Lumineers - Ophelia.mp3': 'Calm',
    'Elton John - Your Song.mp3': 'Calm',

    'Queen - Another One Bites The Dust.mp3': 'Energetic',
    'Imagine Dragons - Radioactive.mp3': 'Energetic',
    'David Guetta - Titanium.mp3': 'Energetic',
    'Foo Fighters - The Pretender.mp3': 'Energetic',
    'Fall Out Boy - My Songs Know What You Did In The Dark.mp3': 'Energetic',
    'Red Hot Chili Peppers - Can\'t Stop.mp3': 'Energetic',
    'Jonas Brothers - Sucker.mp3': 'Energetic',
    'Panic! At the Disco - High Hopes.mp3': 'Energetic',
    'Shakira - Waka Waka.mp3': 'Energetic',
    'Katy Perry - Roar.mp3': 'Energetic',

    'Taylor Swift - You Belong With Me.mp3': 'Happy',
    'Bruno Mars - Treasure.mp3': 'Happy',
    'Pharrell Williams - Freedom.mp3': 'Happy',
    'Jason Mraz - I\'m Yours.mp3': 'Happy',
    'Meghan Trainor - All About That Bass.mp3': 'Happy',
    'OneRepublic - Good Life.mp3': 'Happy',
    'Colbie Caillat - Bubbly.mp3': 'Happy',
    'Justin Bieber - Love Yourself.mp3': 'Happy',
    'Maroon 5 - Sugar.mp3': 'Happy',
    'Owl City - Fireflies.mp3': 'Happy',

    'Adele - Make You Feel My Love.mp3': 'Romantic',
    'Bryan Adams - Everything I do.mp3': 'Romantic',
    'Savage Garden - Truly Madly Deeply.mp3': 'Romantic',
    'Marry Me- Jason Derulo.mp3': 'Romantic',
    'Whitney Houston - I Will Always Love You.mp3': 'Romantic',
    'Shawn Mendes - There\'s Nothing Holdin\' Me Back.mp3': 'Romantic',
    'Christina Perri - A Thousand Years.mp3': 'Romantic',
    'The Beatles - Something.mp3': 'Romantic',
    'Elvis Presley - Love Me Tender.mp3': 'Romantic',
    'Ed Sheeran - Thinking Out Loud.mp3': 'Romantic',

    'Billie Eilish - when the party\'s over.mp3': 'Sad',
    'Lewis Capaldi - Bruises.mp3': 'Sad',
    'Coldplay - The Scientist.mp3': 'Sad',
    'Kodaline - All I Want.mp3': 'Sad',
    'Sam Smith - Stay With Me.mp3': 'Sad',
    'Damien Rice - 9 Crimes.mp3': 'Sad',
    'Bon Iver - Skinny Love.mp3': 'Sad',
    'Adele - All I Ask.mp3': 'Sad',
    'Lana Del Rey - Summertime Sadness.mp3': 'Sad',
    'Sarah McLachlan - Angel.mp3': 'Sad'

}

def load_and_augment(file_path, duration=60):
    #Y = DATA ITSELF
    #SR = SAMPLE RATE (Frequency of the sound)
    y, sr = librosa.load(file_path, duration=duration)
    return [
        y, # ORIGINAL
        librosa.effects.pitch_shift(y=y, sr=sr, n_steps=2),   # CANCION 2 SEMITONOS ARRIBA
        librosa.effects.pitch_shift(y=y, sr=sr, n_steps=-2)   # CANCION 2 SEMITONOS ABAJO
    ]


# ======= EXTRACTION OF FEATURES =======
def extract_features_from_y(y, sr):
    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20), axis=1) #Frequencies of Mel
    chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1) #Musical notes
    spec_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))) #Agudez del sonido (Agudo o grave)
    zero_crossings = float(np.mean(librosa.feature.zero_crossing_rate(y))) #Strong vibrations
    rms = float(np.mean(librosa.feature.rms(y=y))) #Intensity
    rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))) #Energy
    bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))) #Width of the spectrum
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr) #Speed
    tempo = float(tempo)
    
    chroma_cq = librosa.feature.chroma_cqt(y=y, sr=sr)
    key_idx = int(np.argmax(np.mean(chroma_cq, axis=1)))
    
    return np.hstack((
        mfccs,
        chroma,
        np.array([spec_centroid, zero_crossings, rms, rolloff, bandwidth, tempo, key_idx])
    ))



# ======= CREATE THE CSV=======
data = []
labels = []

for filename in os.listdir(folder_path):
    if filename.endswith('.mp3') and filename in file_to_emotion:
        full_path = os.path.join(folder_path, filename)
        try:
            augmented_versions = load_and_augment(full_path)
            for y in augmented_versions:
                sr = 22050  # Librosa forced this sample rate
                features = extract_features_from_y(y, sr)
                data.append(features)
                labels.append(file_to_emotion[filename])
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    else:
        pass 

# ======= SAVE THE CSV =======
df = pd.DataFrame(data)
df['emotion'] = labels
df.to_csv('dataset_music_emotions.csv', index=False)
print("\n\n======New dataset created as 'dataset_music_emotions.csv'.======")

# ======= X = FEATURES Y = TAGS =======
X = df.drop('emotion', axis=1)
y = df['emotion']

# ======= TRAINING =======
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# ======= RANDOM FOREST CLASSIGICATION =======
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=20,
    class_weight='balanced',
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\n\n=== Classification Report ===")
print(classification_report(y_test, y_pred))
print("=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))

# ======= SAVE THE AI MODEL =======
joblib.dump(model, 'music_emotion_model.pkl')
print("\n\n=====AI model trained and saved as 'music_emotion_model.pkl'.=====")