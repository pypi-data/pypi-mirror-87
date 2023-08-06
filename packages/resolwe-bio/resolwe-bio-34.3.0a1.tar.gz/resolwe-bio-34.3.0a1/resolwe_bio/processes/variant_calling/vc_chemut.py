"""CheMut variant calling - GATK joint sample analysis."""
import os

from plumbum import TEE

from resolwe.process import (
    BooleanField,
    Cmd,
    DataField,
    DateField,
    FileField,
    GroupField,
    IntegerField,
    Process,
    SchedulingClass,
    StringField,
)


class CheMutVariantCalling(Process):
    """"CheMut variant calling using multiple BAM input files."""

    slug = "vc-chemut-new"
    name = "Variant calling (CheMut)"
    category = "Other"
    process_type = "data:variants:vcf:chemut"
    version = "3.0.0"
    scheduling_class = SchedulingClass.BATCH
    requirements = {
        "expression-engine": "jinja",
        "executor": {
            "docker": {"image": "broadinstitute/genomes-in-the-cloud:2.3.1-1504795437"}
        },
        "resources": {
            "memory": 16384,
            "cores": 10,
        },
    }
    data_name = "Called variants (CheMut)"

    class Input:
        """Input fields for CheMutVariantCalling."""

        genome = DataField("seq:nucleotide", label="Genome")

        parental_strains = DataField(
            "list:data:alignment:bam", label="Parental strains"
        )

        mutant_strains = DataField("list:data:alignment:bam", label="Mutant strains")

        br_and_ind_ra = BooleanField(
            label="Do variant base recalibration and INDEL realignment",
            default=False,
        )

        dbsnp = BooleanField(
            label="Use dbSNP file",
            default=False,
            description="rsIDs from this file are used to populate the ID column of the output. "
            "Also, the DB INFO flag will be set when appropriate. "
            "dbSNP is not used in any way for the calculations themselves.",
        )

        known_sites = DataField(
            "list:data:variants:vcf",
            label="Known indels",
            required=False,
            hidden="br_and_ind_ra === false",
        )

        class ReadsInformation:
            """Reads information."""

            pl = StringField(
                label="Platform/technology",
                description="Platform/technology used to produce the reads.",
                choices=[
                    ("Capillary", "Capillary"),
                    ("Ls454", "Ls454"),
                    ("Illumina", "Illumina"),
                    ("Helicos", "Helicos"),
                    ("SOLiD", "SOLiD"),
                    ("IonTorrent", "IonTorrent"),
                    ("Pacbio", "Pacbio"),
                ],
                default="Illumina",
            )

            lb = StringField(label="Library", default="x")

            pu = StringField(
                label="Platform unit",
                description="Platform unit (e.g. flowcell-barcode lane for Illumina or slide for "
                "SOLiD). Unique identifier.",
                default="x",
            )

            cn = StringField(
                label="Sequencing center",
                description="Name of sequencing center producing the read.",
                default="x",
            )

            dt = DateField(
                label="Date",
                description="Date the run was produced.",
                default="2017-01-01",
            )

        class VarCallingParameters:
            """Variant calling parameters."""

            stand_emit_conf = IntegerField(
                label="Emission confidence threshold",
                default=10,
                description="The minimum confidence threshold (phred-scaled) at which the program "
                "should emit sites that appear to be possibly variant.",
            )

            stand_call_conf = IntegerField(
                label="Calling confidence threshold",
                default=30,
                description="The minimum confidence threshold (phred-scaled) at which the program "
                "should emit variant sites as called. If a site's associated genotype has a "
                "confidence score lower than the calling threshold, the program will emit the "
                "site as filtered and will annotate it as LowQual. This threshold separates high "
                "confidence calls from low confidence calls.",
            )

            ploidy = IntegerField(
                label="Sample ploidy",
                default=2,
                description="Ploidy (number of chromosomes) per sample. For pooled data, set to "
                "(Number of samples in each pool * Sample Ploidy).",
            )

            glm = StringField(
                label="Genotype likelihoods model",
                description="Genotype likelihoods calculation model to employ -- SNP is the "
                "default option, while INDEL is also available for calling indels and BOTH is "
                "available for calling both together.",
                choices=[
                    ("SNP", "SNP"),
                    ("INDEL", "INDEL"),
                    ("BOTH", "BOTH"),
                ],
                default="SNP",
            )

            intervals = StringField(
                label="Intervals",
                description="Use this option to perform the analysis over only part of the "
                "genome. This argument can be specified multiple times. You can use "
                "samtools-style intervals (e.g. -L chr1 or -L chr1:100-200).",
                required=False,
            )

            rf = BooleanField(
                label="ReasignOneMappingQuality Filter",
                description="This read transformer will change a certain read mapping quality to "
                "a different value without affecting reads that have other mapping qualities. "
                "This is intended primarily for users of RNA-Seq data handling programs such as "
                "TopHat, which use MAPQ = 255 to designate uniquely aligned reads. "
                "According to convention, 255 normally designates unknown quality, and most "
                "GATK tools automatically ignore such reads. By reassigning a different mapping "
                "quality to those specific reads, users of TopHat and other tools can circumvent "
                "this problem without affecting the rest of their dataset.",
                default=False,
            )

        reads_info = GroupField(ReadsInformation, label="Reads information")

        varc_param = GroupField(
            VarCallingParameters, label="Parameters of UnifiedGenotyper"
        )

    class Output:
        """Output fields for CheMutVariantCalling."""

        vcf = FileField(label="Called variants file")
        tbi = FileField(label="Tabix index")
        species = StringField(label="Species")
        build = StringField(label="Build")

    def run(self, inputs, outputs):
        """Run analysis."""
        if inputs.br_and_ind_ra and not inputs.known_sites and not inputs.known_indels:
            self.error(
                "Variant base recalibration and INDEL realignment step requires known sites/indels "
                "information in the form of user provided VCF files."
            )

        parental_samples = [bam.entity.name for bam in inputs.parental_strains]
        mutant_samples = [bam.entity.name for bam in inputs.mutant_strains]
        if len(parental_samples + mutant_samples) != len(
            set(parental_samples + mutant_samples)
        ):
            self.error("Sample names must be unique.")

        basename = os.path.basename(inputs.genome.output.fasta.path)
        assert basename.endswith(".fasta")
        genome_name = basename[:-6]

        COUNTER = 1

        for bam in inputs.parental_strains + inputs.mutant_strains:
            basename = os.path.basename(bam.output.bam.path)
            assert basename.endswith(".bam")
            bam_file = basename[:-4]

            # MarkDuplicates
            args = [
                f"java -Xmx{self.requirements.resources.memory // 1024}g",
                "-jar /usr/gitc/picard.jar",
                "MarkDuplicates",
                f"I={bam_file}",
                f"O={bam_file}_inds.bam",
                "METRICS_FILE=junk.txt",
                "VALIDATION_STRINGENCY=LENIENT",
            ]

            return_code, _, _ = Cmd[args] & TEE(retcode=None)
            if return_code:
                self.error("MarkDuplicates tool failed.")

            # AddOrReplaceReadGroups
            sample_type = "parental"
            if bam in inputs.mutant_strains:
                sample_type = "mut"

            args = [
                "java -jar /usr/gitc/picard.jar",
                "AddOrReplaceReadGroups",
                f"I={bam_file}_inds.bam",
                f"O={bam_file}_indh.bam",
                f"RGID=ReadGroup_{COUNTER}",
                f"RGLB={inputs.reads_info.lb}",
                f"RGPL={inputs.reads_info.pl}",
                f"RGPU={inputs.reads_info.pu}",
                f"RGSM={sample_type}_{bam_file}",
                f"RGCN={inputs.reads_info.cn}",
                f"RGDT={inputs.reads_info.dt}",
            ]

            return_code, _, _ = Cmd[args] & TEE(retcode=None)
            if return_code:
                self.error("AddOrReplaceReadGroups tool failed.")

            # Index bam file
            return_code, _, _ = Cmd["samtools"]["index"][f"{bam_file}_indh.bam"] & TEE(
                retcode=None
            )
            if return_code:
                self.error("Samtools indexing failed.")
            COUNTER = COUNTER + 1

        self.progress = 0.4
