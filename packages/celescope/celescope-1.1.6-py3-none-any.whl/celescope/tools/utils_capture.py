import os
from collections import defaultdict
import celescope
import pysam
import numpy as np
import pandas as pd
from celescope.tools.utils import format_number, log, read_barcode_file
from celescope.tools.utils import format_stat
from celescope.tools.utils import read_one_col, gene_convert, glob_genomeDir
from celescope.tools.report import reporter


class SplitBAM():

    def __init__(self, sample, outdir, bam, barcodes, gtf, gene_list_file=None):
        self.sample = sample
        self.outdir = outdir
        self.bam = bam
        self.barcodes = barcodes
        self.gtf = gtf
        self.gene_list_file = self.gene_list_file

    def umi_correction():
        pass

    def get_cell_index():
        pass

    @classmethod
    def get_gene_id_name_dict():
        pass   

        

    def split_bam(bam, barcodes, outdir, sample, gene_id_name_dic, min_query_length):
        '''
        input:
            bam: bam from feauturCounts
            barcodes: cell barcodes, set
            gene_id_name_dic: id name dic
            min_query_length: minimum query length

        ouput:
            bam_dict: assign reads to cell barcodes and UMI
            count_dict: UMI counts per cell
            index: assign index(1-based) to cells
        '''

        # init
        count_dict = defaultdict(dict)
        bam_dict = defaultdict(list)
        index_dict = defaultdict(dict)
        cells_dir = f'{outdir}/cells/'

        # read bam and split
        split_bam.logger.info('reading bam...')
        samfile = pysam.AlignmentFile(bam, "rb")
        header = samfile.header
        barcodes = list(barcodes)
        barcodes.sort()
        for read in samfile:
            attr = read.query_name.split('_')
            barcode = attr[0]
            umi = attr[1]
            if not read.has_tag('XT'):
                continue
            gene = read.get_tag('XT')
            query_length = read.infer_query_length()
            if (barcode in barcodes) and (gene in gene_id_name_dic) and (query_length >= min_query_length):
                gene_name = gene_id_name_dic[gene]
                read.set_tag(tag='GN', value=gene_name, value_type='Z')
                index = barcodes.index(barcode) + 1
                read.set_tag(tag='CL', value=f'CELL{index}', value_type='Z')

                # assign read to barcode
                bam_dict[barcode].append(read)

                # count
                if gene_name not in count_dict[barcode]:
                    count_dict[barcode][gene_name] = {}
                if umi in count_dict[barcode][gene_name]:
                    count_dict[barcode][gene_name][umi] += 1
                else:
                    count_dict[barcode][gene_name][umi] = 1

        split_bam.logger.info('writing cell bam...')
        # write new bam
        index = 0
        for barcode in barcodes:
            # init
            index += 1
            index_dict[index]['barcode'] = barcode
            index_dict[index]['valid'] = False

            # out bam
            if barcode in bam_dict:
                cell_dir = f'{cells_dir}/cell{index}'
                cell_bam_file = f'{cell_dir}/cell{index}.bam'
                if not os.path.exists(cell_dir):
                    os.makedirs(cell_dir)
                index_dict[index]['valid'] = True
                cell_bam = pysam.AlignmentFile(
                    f'{cell_bam_file}', "wb", header=header)
                for read in bam_dict[barcode]:
                    cell_bam.write(read)
                cell_bam.close()

        # out df_index
        df_index = pd.DataFrame(index_dict).T
        df_index.index.name = 'cell_index'
        index_file = f'{outdir}/{sample}_cell_index.tsv'
        df_index.to_csv(index_file, sep='\t')

        # out count_dict
        df_count = pd.DataFrame(columns=['barcode', 'gene', 'UMI', 'read_count'])
        for barcode in count_dict:
            for gene in count_dict[barcode]:
                for umi in count_dict[barcode][gene]:
                    read_count = count_dict[barcode][gene][umi]
                    df_count = df_count.append({
                        'barcode': barcode,
                        'gene': gene,
                        'UMI': umi,
                        'read_count': read_count,
                    }, ignore_index=True)
        count_file = f'{outdir}/{sample}_count.tsv'
        df_count.to_csv(count_file, sep='\t', index=False)

        return index_file, count_file