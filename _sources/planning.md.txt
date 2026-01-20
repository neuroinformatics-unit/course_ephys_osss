# Course Plan

## A tentative plan

This is a tenative plan to see how the course would look within the alloted
time frame. It is flexible, let's discuss if anything any 
content should be moved or replaced.

### Monday morning (10:00-13:00) : Introduction

**Goal** 
- Provide a high-level overview of the main concepts in extracellular electrophysiology, of which 
we will fill in the details over the next few days. 
- Give a general introduction to SpikeInterface
- Provide a simple, full SpikeInterface pipeline that they can use for reference for the coming days

**Plan:**

*10:00 - 10:15* : Welcome, housekeeping, overview of the course, downloading the example data

*10:15 - 10:45* : (lecture, Joe) A high-level introduction to extracellular electrophysiology:
- Purpose of electrophysiology recordings (+ some famous results)
- Probe evolution (tetrodes to high-density).
- Introduction to the data (probe channels -> timeseries, time x channel data)
- Very brief overview of the pipeline (preprocessing, sorting, quality metrics). What the steps are,
why we do them and how they result in data (spike times from good units) that are used in papers.

*10:45 - 11:45* : (coding) Coding up a very simple pipeline and exploring the data.
- Quick introduction to SpikeInterface (e.g. history and purpose)
- Loading data in SpikeInterface
- SpikeInterface objects
- Loading and visualising the probe
- Visualising the raw data
- Implementing a simple preprocessing pipeline (phase shift, filter, CMR)

*11:45 - 12:05* : (lecture, Olivier?) A deeper introduction to electrophysiological data
- ADC sampling, sampling theory (quick introduction to sine, cosine functions and the Fourier transform / Power spectrum)
- Saturation and bit depth

*12:05 - 13:00* :  (coding) Implement the rest of the pipeline (sorting, sorting analyzer, quality metrics)

(depending on how things are going, we could swap the last two, having a very long coding period and ending on the lecture)

**Example data required** 

A very short (1-2 s) recording that can be quickly run through the entire pipeline.

### Tuesday morning (10:00 - 13:00) : Preprocessing

**Goal**

They should have a good understanding of how to implement common and state-of-the-art
preprocessing steps, and at least some intuition as to the underlying theory.

**Plan**

*10:00-10:30* : (lecture, Joe?) Talk on the theory of preprocessing steps 
- phase shift, bandpass, CMR
- whitening
- drift correction
- running preprocessing steps in SpikeInterface vs. the sorter (e.g. kilosort)
- filter edge effects, chunking
- lazy data access
- always look at your data

*10:30 - 11:30* : (coding) Add whitening and drift correction to the pipeline. Visualise before vs. after.
Exploring motion outputs (e.g. drift maps)
If this is remaining time, a stretch goal can be a quick talk on 
spatial highpass filter, and running it in SpikeInterface.

*11:30 - 12:00* : (lecture, Olivier?) Lecture on advanced preprocessing 
(bad channel detection, raw data quality metrics, saturation detection)

*12:00 - 13:00* : (coding) Adding these steps to the pipeline.

**Example data required**

We could use the same as Monday, but for this data it's not necessary it needs to be sortable.
Maybe a good example for bad-channel detection, saturation or raw-data quality metrics would be good.
We could have a good example and a bad example.


### Tuesday afternoon (14:00-17:00) : Sorting

**Goal**

By the end of this session they should have a strong idea of the purpose of sorting, 
key concepts (spike times, unit assignment, templates, waveforms / snippets). 
Know the names of a few different sorters and how to compare them. 
Understand the possible approaches to multi-session recordings, gain experience with UnitMatch.

**Plan**

*14:00 - 14:30* : (lecture, Alessio?) Overview of sorting
- Why we need to do it
- The key outputs (spike times, unit assignment, templates (also can mention waveforms / snippets))
- It is a hard problem - many sorters exist
- We can use spikeinterface to run and compare various sorters

*14:30 - 15:30* : (coding) Run a couple of different sorters in SpikeInterface and compare the outputs using sorting comparison.
We can leave it a little up to the user, but KS4 and Lupin seem a good pair to use in the example.
We can go into more detail here the options to run preprocessing steps in SpikeInterface vs. the sorter,
as well as introduce sorting components.

*15:30 - 16:00* : (lecture, Alessio / Sam?) Deep dive into the black box, the general steps behind a sorter 
(peak detection, clustering, template matching etc.)

*16:00 - 17:00* : (lecture / coding, Enny) UnitMatch
A 20-minute talk and 40 minute implementation? Happy to extend if this is not enough time

**Example data required**

Here we can use short data that sorts quickly, but it would be nice if it wasn't all junk units.
We could try and use the same data as on Monday. 
For UnitMatching, the sorting outputs from two sessions would work. 

### Wednesday morning (10:00 - 13:00) : Assessing Sorting Quality

**Goal**

- Understand why we need to sort and key concepts (e.g. splits, merges)
- Understand a few of the main quality metrics
- Know how to compute / threshold quality metrics in SpikeInterface and 
perform manual curation in the spikeinterface-gui

**Plan**

*10:00 - 10:30* : (lecture, Chris/Julie?) Introduction to assessing sorting quality
- Why we need to do it, splits and merges, good/noise/mua clusters
- Quality metrics, and some detail on the main ones (e.g. refractory period, amplitude cutoff, cluster space metrics)

*10:30 - 11:45* : (coding)
- Use the sorting analyzer to compute metrics
- Using Bombcell through SpikeInterface
- Using UnitRefine through SpikeInterface

*11:45 - 12:05* : (lecture, Chris?) Overview of SpikeInterface GUI (e.g. what the different plots mean)

*12:05 - 13:00* : (coding) walkthrough / free time to curate a dataset in spikeinterface-gui


**Example data required**

We will need a small toy dataset that they can quickly create and run a sorting analyzer on.
But it should have a few good units, so will be as small as possible while being useful.
For the spikeinterface-GUI, we can just use the sorting output of a larger dataset.

### Wednesday afternoon (14:00-17:00) : Analysing Outputs

**Plan**

Something like?:

- 20-30 minute talk on different types of extracellular ephys analysis. Some real use cases / papers
- 20-30 minutes on walkthrough time alignment
- 30 minutes: give a sorting output and some behavioural event times, construct a histogram 'by hand'
- rest of the session (~2h) on using Pynapple?

## General thoughts on course structure / content

- During the coding periods, we can walk through the code step-by-step for core pipeline, then have periods
for those to do extra exercises (e.g. 'Use get traces to get scaled and unscaled raw data', 'Plot data before and after whitening' etc.'. 
This way those with less experience have a solid grounding, and those with more experience can go ahead and start on the exercises.
- We can have a lot of exercises, from easy to harder, to keep everyone busy. There is no obligation for them to complete these,
it is just a tool for learning / prompting questions.
- The code will be presented through  Quarto, either through slides (e.g. here) or a book-like format (e.g. here), lets discuss. 
- The benefit of the latter is we end up with a really nice handbook that should be generally useful.
- The coding periods will be interleaved with short (20-30 minute) lectures to discuss the theory.
- There will be a range of backgrounds and while we can assume basic Python knowledge, we cannot assume too
much background in ephys / neuroscience / DSP. This is not a problem, we can still discuss advanced topics, we
will just need to make sure to build to these from the ground-up.
- Their laptops may range in performance, where possible we should endeavour to use the smallest example data possible.

## Other notes

- Having a 10-minute end-of-session discussion / recap might be a nice idea

```{toctree}
:maxdepth: 2
:caption: Sections

```
