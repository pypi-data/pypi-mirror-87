"""Divides the population into species based on genomic distances."""
from itertools import count

from neat.config import ConfigParameter, DefaultClassConfig
from neat.math_util import mean, stdev


class Species(object):
    """
    各種族のクラス
    種族のキーや代表者やメンバー
    おそらく平均の適応度などを保存する
    """

    def __init__(self, key, generation):
        self.key = key
        self.created = generation
        self.last_improved = generation
        self.representative = None
        self.members = {}
        self.fitness = None
        self.adjusted_fitness = None
        self.fitness_history = []

    def update(self, representative, members):
        self.representative = representative
        self.members = members

    def get_fitnesses(self):
        return [m.fitness for m in self.members.values()]


class GenomeDistanceCache(object):
    """
    Genome同士の距離をキャッシュするためのクラス
    辞書に任意の2個のGenomeの距離をキャッシュできるようになっている
    おそらく効率性をあげるため
    """

    def __init__(self, config):
        self.distances = {}
        self.config = config
        self.hits = 0
        self.misses = 0

    def __call__(self, genome0, genome1):
        g0 = genome0.key
        g1 = genome1.key
        d = self.distances.get((g0, g1))
        if d is None:
            # Distance is not already computed.
            # 2つのgenomeの距離を計算する
            d = genome0.distance(genome1, self.config)
            self.distances[g0, g1] = d
            self.distances[g1, g0] = d
            self.misses += 1
        else:
            self.hits += 1

        return d


class DefaultSpeciesSet(DefaultClassConfig):
    """
    Encapsulates the default speciation scheme.

    基本的な種族分類を行う 種族のSetクラス
    """

    def __init__(self, config, reporters):
        # pylint: disable=super-init-not-called
        self.species_set_config = config
        self.reporters = reporters
        self.indexer = count(1)
        self.species = {}
        self.genome_to_species = {}

    @classmethod
    def parse_config(cls, param_dict):
        return DefaultClassConfig(param_dict,
                                  [ConfigParameter('compatibility_threshold', float)])

    def speciate(self, config, population, generation):
        """
        ゲノムを遺伝的類似度によって種に配置する。
        この方法は、現在の種の代表者が旧世代のものであると仮定しており、種分化が行われた後、旧世代の代表者は削除され、新世代の代表者と入れ替わるべきであることに注意してください。
        この仮定に違反した場合は、コードの他の必要な部分が新しい動作を反映するように更新されていることを確認してください。
        """
        assert isinstance(population, dict)

        compatibility_threshold = self.species_set_config.compatibility_threshold

        # Find the best representatives for each existing species.

        unspeciated = set(population)
        distances = GenomeDistanceCache(config.genome_config)
        new_representatives = {}
        new_members = {}

        # 1世代前の種族ごと
        # このforでは１世代前の種族の代表に最も近い新しい代表者を取り出しているだけ（他のメンバは取り出していない）
        for sid, s in self.species.items():
            # sid = 種族のキー  種族クラス (Species)
            candidates = []

            # genomeのID=gid
            for gid in unspeciated:
                g = population[gid]

                # sの代表者とgenome gの距離を計算
                d = distances(s.representative, g)
                candidates.append((d, g))

            # The new representative is the genome closest to the current representative.
            # sの代表者と最も距離が近いgenomeを取り出す rdistが距離 repが新しい代表者genome
            ignored_rdist, new_rep = min(candidates, key=lambda x: x[0])
            new_rid = new_rep.key
            new_representatives[sid] = new_rid
            new_members[sid] = [new_rid]
            unspeciated.remove(new_rid)

        # Partition population into species based on genetic similarity.
        # まだ分類していないgenomeたちを類似度を用いて　代表者に近いものに割り振っていく
        # ただし似ていないものは新しいものにする


        while unspeciated:
            gid = unspeciated.pop()
            g = population[gid]

            # Find the species with the most similar representative.
            candidates = []
            for sid, rid in new_representatives.items():
                rep = population[rid]
                d = distances(rep, g)

                # もしある種族の代表者repと gの類似度が似ているなら候補にいれる
                if d < compatibility_threshold:
                    candidates.append((d, sid))

            # 複数の種族に入ることができるときは最も近い代表のグループに入れる
            if candidates:
                ignored_sdist, sid = min(candidates, key=lambda x: x[0])
                new_members[sid].append(gid)
            else:
                # No species is similar enough, create a new species, using
                # this genome as its representative.
                # 新しく代表を作る
                sid = next(self.indexer)
                new_representatives[sid] = gid
                new_members[sid] = [gid]

        # Update species collection based on new speciation.
        # 種族コレクションを新しく出来たSpeciationをもとに更新する
        self.genome_to_species = {}
        for sid, rid in new_representatives.items():

            # 今の世代の種族のID=sidとして　もし前世代にもあるならその種族s=speciesとする
            # 各種族のSpeciesインスタンスを SpeciesSetのspecies辞書に入れる（単語が似ていて厄介）
            s = self.species.get(sid)
            if s is None:
                s = Species(sid, generation)
                self.species[sid] = s

            members = new_members[sid]
            for gid in members:
                self.genome_to_species[gid] = sid

            member_dict = dict((gid, population[gid]) for gid in members)

            # 新しい種族sの代表者とそのメンバーをsに更新する
            s.update(population[rid], member_dict)

        gdmean = mean(distances.distances.values())
        gdstdev = stdev(distances.distances.values())
        self.reporters.info(
            'Mean genetic distance {0:.3f}, standard deviation {1:.3f}'.format(gdmean, gdstdev))

    def get_species_id(self, individual_id):
        return self.genome_to_species[individual_id]

    def get_species(self, individual_id):
        sid = self.genome_to_species[individual_id]
        return self.species[sid]
