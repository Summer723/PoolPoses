# To-Do List

- [] Related work section 
- [] Model Architecture
- []
- 



# Project Preparation Checklist

 - [x] Describe a well-defined problem. State concrete steps to proceed instead of vague ideas.
     * problem definition
     * related work
     * what challenges do you expect?
     * what challenges do you want to work/focus on?
 - [ ] Make sure you have all the tools you need
     * open source code, unless re-implementation is your goal
     * GPU resources for training
        * GPU memory consumption
        * how long does related work train and on what hardware?
        * can you simplify your problem, work on low-res images?
     * training data
        * sufficient number of examples?
        * labeled examples (unless you work on self-supervision)?
        * is the dataset legal/ethical?
            * scraping images from the web without explicit permission from the depicted person to use for ML training is not OK!
        * some datasets require registration; get access ASAP
 - [ ] Think about how to evaluate your method
     * which metrics can be used?
     * plan with quantitative and qualitative comparisons
 - [ ] Manage your time for design, development, evaluation, and writing.
     * roughly allocate equal amounts of time for each of the four aspects
 - [ ] Design tasks such that they can be split into as independent blocks as possible, such that your team can work in parallel.

 # Project Submission Checklist
 
 - [ ] State the team members and their individual contributions
    * everybody must be involved in the project design/planning, do some coding, as well as some writing.
    * state contributions explicitly, e.g., "Eva experimented with different loss functions for self-supervision and wrote the dataloader. She wrote the related work section and conclusion. Adam experimented with different network architectures and extended them with the new Affine layer. He wrote Section 1 and 5. All team members met weekly to discuss the project ideas, progress on individual components, and polished the final writeup into a cohesive story." 
 - [ ] Report structure
	* Do you have all relevant sections (abstract, contributions, intro, related work, method section, evaluation, limitations/future work/conclusion)?
	* Are all sections cohearent and with little redundency? Bring the whole document into a cohesive story. This likely requires you to re-visit the related work and method sections that you wrote earlier.
 - [ ] Writeup
    * Don't copy paste from anywhere. Every sentence must be yours unless in quotation marks.
         * Still, read other papers and follow a similar style where appropriate. Be inspired but don't copy.
    * It is good to re-use existing code/approaches as much as possible, but:
         * Write clearly which parts come from you "We propose/implemented/define ..."
         * Write clearly where you got ideas from "This idea is inspired by/based on the BigGAN approach by Smarty et al. [12]."
         * State which source code was used. "We based our code on Smarty et al. [12] <URL> which makes simplifying assumptions on the light sources and extend it with differentiable shadow handling."
         * Cite the origin whenever you re-use or modify existing figures/images.
    * Is the problem well-motivated in the introduction?
    * Is the most related work covered in the related work section? Not just a list of papers, explain what that work is doing and how it differs to yours.
    * Are all model components explained in the method section? Create a pipeline figure for an easy overview.
         * Have equations if useful, explain all variables, pay attention to proper math formatting.
    * Are datasets and metrics explained in the evaluation
         * Train/Val/Test set splits
         * precise definition of evaluation criteria/metrics
		 * training details (batch size, optimizer, learning rate...)
    * Is the main contribution analyzed, an ablation study?
    * State limitations
    * Conclude with the main finding of your story
    * Proofread for typos and grammar. Double-check math formatting! 
 - [ ] Code
    * bundle all code as a .zip file.
    * make sure that every team member understands the code from the others and is able to explain it.
    * provide links to the used datasets
         * upload your dataset (e.g, to google drive) and link it if you created a new one.
 - [] Upload writeup and code in a single .zip file to Canvas. All group members must agree to the submission.
