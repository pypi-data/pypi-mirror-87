# SPDX-License-Identifier: GPL-3.0-only
# SPDX-FileCopyrightText: 2020 Vincent Lequertier <vi.le@autistici.org>

from collections import Counter
import time
from typing import Dict, List, Union
from bs4 import BeautifulSoup
import networkx as nx
import requests
from matplotlib import cm
from matplotlib.colors import to_hex
import numpy as np
import plotly.colors
import plotly.graph_objects as go
from sklearn import preprocessing
from Levenshtein import distance
from urllib3.util.retry import Retry


class CoCitation:
    """
    Create a co-citation graph

    """

    def __init__(
        self,
        articles_list: List[str],
        sd_api_key: str = "",
        graph: str = "",
        wait: int = None,
        retries: int = None,
        data_type: str = "journal",
    ):
        """
        Instantiate the co-citation graph

        Args:
            articles_list (list): The list of articles URL. At the moment only arXiv,
            ScienceDirect and PubMed are supported
            sd_api_key (str): The key to query the ScienceDirect API
            graph (str): A saved netowrkx weighted graph file (optional)
            wait (int): Number of seconds to wait between API call to workaround
            API call thresholds( optional)
            data_type (str): Type of data (journal, article, or institution)
        """
        self.sd_api_key = sd_api_key
        self.jour_abbrevs = self.load_abbreviations()
        self.wait = wait

        self.re_session = requests.Session()

        if retries:
            self.re_session.mount(
                "https://",
                requests.adapters.HTTPAdapter(
                    max_retries=Retry(total=retries, backoff_factor=0.5)
                ),
            )

        if data_type not in ["journal", "article", "institution"]:
            raise ValueError("data_type must be 'journal', 'article'")

        if data_type == "institution" and any(
            [
                "sciencedirect" in article_url or "arxiv" in article_url
                for article_url in articles_list
            ]
        ):
            raise NotImplementedError(
                "institution data type is not supported for sciencedirect or arxiv articles"
            )

        self.type = data_type

        if not sd_api_key and any(
            ["sciencedirect" in article_url for article_url in articles_list]
        ):
            raise ValueError(
                "Missing ScienceDirect API key and at least one article is from ScienceDirect"
            )

        if graph:
            self.co_citation_graph = nx.read_weighted_edgelist(
                graph, nodetype=str, delimiter="\t"
            )
            self.co_citation_graph = self.init_nodes_weight(self.co_citation_graph)
        else:
            self.co_citation_graph = self.create_citation_graph(articles_list)

    @staticmethod
    def load_abbreviations() -> Dict[str, str]:
        """
        Get journal abbreviations

        Returns:
            dict: The abbreviations
        """
        abbreviations = {}
        with open("abbreviations.txt", "r") as fh:
            for line in fh.readlines():
                k, v = line.split("\t")
                abbreviations[k.lower()] = v.strip()

        return abbreviations

    def create_citation_graph(self, articles_list: List[str]) -> nx.Graph:
        """
        1. Get the references of each article and their corresponding data\
        (journal, article or institution)
        2. Generate the co-citation pairs and add them the graph. The weights are the\
        number of times the data are co-cited.

        Args:
            articles_list (list): The list of articles URL. At the moment only arXiv,
                ScienceDirect and PubMed are supported

        Returns:
            list: The pairs
        """
        graph = nx.Graph()
        for article in articles_list:
            if self.wait:
                time.sleep(self.wait)
            citations = self.get_citations(article)
            citations = list(filter(lambda c: c != "", citations))
            pairs = self.gen_perms(citations)
            for j1, j2, w in pairs:
                graph.add_edge(
                    j1,
                    j2,
                    weight=w
                    if not graph.has_edge(j1, j2)
                    else graph[j1][j2]["weight"] + w,
                )

        graph = self.init_nodes_weight(graph)

        return graph

    @staticmethod
    def gen_perms(citations: List[str]) -> List[List[Union[str, int]]]:
        """
        Get all pair commutative permutations of a list

        Args:
            citations (list): The list of journal citations
        Returns:
            list: The pairs
        """
        pairs = []
        counts = Counter(citations)
        for i in range(len(citations)):
            for j in range(i + 1, len(citations)):
                pairs.append(
                    [
                        citations[i],
                        citations[j],
                        min(counts[citations[i]], counts[citations[j]]),
                    ]
                )

        return pairs

    @staticmethod
    def init_nodes_weight(graph: nx.Graph) -> nx.Graph:
        """
        Init the nodes weight. The weight are the sum of the connected edges
        weights

        Args:
            graph (nx.Graph): The graph
        Returns:
            list: The graph with the initialized nodesj weight
        """
        for node in graph.nodes():
            graph.nodes[node]["weight"] = sum(
                graph[node][neighbor]["weight"]
                for neighbor in list(graph.neighbors(node))
            )

        return graph

    @staticmethod
    def rm_dupes(lst: List[str], threshold: int) -> List[str]:
        """https://stackoverflow.com/a/14229397
        Remove duplicates in a list that have a Levenshtein distance below the
        threshold
        """
        items = []
        while lst:
            center = lst[0]
            items.append(center)
            lst = [word for word in lst if distance(center, word) >= threshold]

        return items

    def get_article_title_pubmed(self, article_url: str) -> str:
        """
        Get the title of a pubmed article

        Args:
            article_url (str): The URL of the article.
        Returns:
            str: The article's title
        """

        pmid = article_url.split("/")[-1]
        url = (
            "https://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.cgi?db=pubmed&retmode=xml&id="
            + pmid
        )
        xml_parsed = BeautifulSoup(self.re_session.get(url).text, features="lxml")
        authors = xml_parsed.find_all("author")
        year = xml_parsed.find("year").text
        if len(authors) > 2:
            return (
                authors[0].initials.text
                + ". "
                + authors[0].lastname.text
                + " et al. ("
                + year
                + ")"
            )
        else:
            return (
                " and ".join(
                    [
                        author.initials.text + ". " + author.lastname.text
                        for author in authors
                    ]
                )
                + " "
                + year.join(["(", ")"])
            )

    @staticmethod
    def get_article_title_sem_scholar(ref: dict) -> str:
        """
        Get the title of an article indexed in semanticscholar

        Args:
            ref (dict): An article reference
        Returns:
            str: The article's title
        """
        if len(ref["authors"]) > 2:
            return (
                ref["authors"][0]["name"]
                + " et al. "
                + str(ref["year"]).join(["(", ")"])
            )
        else:
            return (
                " and ".join([author["name"] for author in ref["authors"]])
                + " "
                + str(ref["year"]).join(["(", ")"])
            )

    def get_article_institution_pubmed(self, article_url: str) -> List[str]:
        """
        Get the institutions of an article indexed in semanticscholar

        Args:
            article_url (str): A pubmed article url
        Returns:
            List[str]: The article's institutions
        """
        pmid = article_url.split("/")[-1]
        url = (
            "https://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.cgi?db=pubmed&retmode=xml&id="
            + pmid
        )
        return self.rm_dupes(
            list(
                {
                    aff.text.split(",")[1].strip(" ") if "," in aff.text else aff.text
                    for aff in BeautifulSoup(
                        self.re_session.get(url).text, features="lxml"
                    ).find_all("affiliation")
                }
            ),
            5,
        )

    def get_journal_pubmed(self, article_url: str) -> str:
        """
        Get the journal of an article

        Args:
            article_url (str): The URL of the article. At the moment only arXiv,
                ScienceDirect and PubMed are supported
        Returns:
            str: The journal's name
        """
        pmid = article_url.split("/")[-1]
        url = (
            "https://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.cgi?db=pubmed&retmode=xml&id="
            + pmid
        )
        return (
            BeautifulSoup(self.re_session.get(url).text, features="lxml")
            .find("isoabbreviation")
            .text
        )

    def get_journal_sem_scholar(self, ref: dict) -> str:
        """
        Get the journal of an article

        Args:
            ref (dict): A semanticscholar referece
        Returns:
            str: The journal's name
        """
        return (
            self.jour_abbrevs[ref["venue"].lower()]
            if ref["venue"].lower() in self.jour_abbrevs
            else ref["venue"]
        )

    def get_citations(self, article_url: str) -> List[str]:
        """
        Get all citations data for an article

        This function does two things:

        1. Get the citations
        2. For each citation, get the data (journal or artilce)

        Args:
            article_url (str): The URL of the article. At the moment only arXiv,
                ScienceDirect and PubMed are supported
        Returns:
            list: The list of citations
        """
        if (
            "pubmed" not in article_url
            and "arxiv" not in article_url
            and "sciencedirect" not in article_url
        ):
            raise NotImplementedError("URL {} not implemented".format(article_url))
        if "pubmed" in article_url:
            pmid = article_url.split("/")[-1]
            url = (
                "https://www.ncbi.nlm.nih.gov/entrez/eutils/elink.cgi?db=pubmed&linkname=pubmed_pubmed&retmode=xml&id="
                + pmid
            )
            if self.type == "journal":
                return [
                    self.get_journal_pubmed(
                        "https://www.ncbi.nlm.nih.gov/pubmed/" + idx.text
                    )
                    for idx in BeautifulSoup(
                        self.re_session.get(url).text, features="lxml"
                    ).linksetdb.find_all("id")
                    if self.wait is None
                    or (self.wait is not None and time.sleep(self.wait) is None)
                ]
            elif self.type == "article":
                return [
                    self.get_article_title_pubmed(
                        "https://www.ncbi.nlm.nih.gov/pubmed/" + idx.text
                    )
                    for idx in BeautifulSoup(
                        self.re_session.get(url).text, features="lxml"
                    ).linksetdb.find_all("id")
                    if self.wait is None
                    or (self.wait is not None and time.sleep(self.wait) is None)
                ]
            else:
                return [
                    y
                    for idx in BeautifulSoup(
                        self.re_session.get(url).text, features="lxml"
                    ).linksetdb.find_all("id")[:5]
                    for y in self.get_article_institution_pubmed(
                        "https://www.ncbi.nlm.nih.gov/pubmed/" + idx.text
                    )
                    if self.wait is None
                    or (self.wait is not None and time.sleep(self.wait) is None)
                ]
        if "arxiv" in article_url:
            idx = article_url.split("/")[-1].rstrip()
            url = "https://api.semanticscholar.org/v1/paper/arxiv:" + idx
            refs = self.re_session.get(url).json()["references"]
        if "sciencedirect" in article_url:
            pii = article_url.split("/")[-1].rstrip()
            doi = (
                BeautifulSoup(
                    self.re_session.get(
                        "https://api.elsevier.com/content/article/pii/"
                        + pii
                        + "?httpAccept=text/xml&APIKey="
                        + self.sd_api_key
                    ).text,
                    features="lxml",
                )
                .find("prism:doi")
                .text
            )
            url = "https://api.semanticscholar.org/v1/paper/" + doi
            refs = self.re_session.get(url).json()["references"]

        if self.type == "journal":
            return [self.get_journal_sem_scholar(ref) for ref in refs]
        else:
            return [self.get_article_title_sem_scholar(ref) for ref in refs]

    def get_edge_trace(self) -> List[go.Scatter]:
        """
        Generate the edges trace. The colors corresponds to the edge weights

        Returns:
            list: The list of edges trace
        """

        edges_trace = []
        greys = cm.get_cmap("Greys", 12)
        weights = list(
            nx.get_edge_attributes(self.co_citation_graph, "weight").values()
        )
        weights = (
            preprocessing.normalize(np.array(weights).reshape(1, -1)) * 50
        ).flatten()
        colors = greys(weights)
        for idx, edge in enumerate(self.co_citation_graph.edges(data=True)):
            x0, y0 = self.co_citation_graph.nodes[edge[0]]["pos"]
            x1, y1 = self.co_citation_graph.nodes[edge[1]]["pos"]
            edges_trace.append(
                go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode="lines",
                    line=dict(width=1.5, color=to_hex(colors[idx])),
                )
            )

        return edges_trace

    def get_node_trace(self) -> dict:
        """
        Generate the nodes trace. The colors corresponds to the sum edge weights
        connected to the noes

        Returns:
            dict: The nodes trace
        """
        node_x = []
        node_y = []
        for node in self.co_citation_graph.nodes():
            x, y = self.co_citation_graph.nodes[node]["pos"]
            node_x.append(x)
            node_y.append(y)

        node_sizes = list(
            nx.get_node_attributes(self.co_citation_graph, "weight").values()
        )

        return dict(
            x=node_x,
            type="scatter",
            y=node_y,
            text=list(self.co_citation_graph.nodes),
            textposition="top center",
            mode="markers+text",
            textfont={"family": "sans serif", "size": 21, "color": "#000000"},
            marker=dict(
                colorscale=plotly.colors.sequential.Greys[2:],
                reversescale=False,
                color=node_sizes,
                size=16,
                line_width=0,
                line=None,
            ),
        )

    def plot_graph(self, display=True, k=20) -> None:
        """
        Plot the co-citation graph

        Args:
            display (bool): If True, view the plot in a web browser, else write
                the plot to disk
            k (int): Minimal distance between nodes
        """

        if len(self.co_citation_graph.nodes()) == 0:
            raise ValueError("Graph is empty")
        pos = nx.spring_layout(self.co_citation_graph, k=k)
        nx.set_node_attributes(self.co_citation_graph, pos, "pos")

        edges_trace = self.get_edge_trace()
        node_trace = self.get_node_trace()

        fig = go.Figure(
            data=edges_trace + [node_trace],
            layout=go.Layout(
                title={
                    "text": "Co-citation graph",
                    "y": 0.9999,
                    "x": 0.5,
                    "font_size": 30,
                    "font": {"family": "sans serif", "color": "#000000"},
                    "xanchor": "center",
                    "yanchor": "top",
                },
                showlegend=False,
                plot_bgcolor="rgba(26,150,65,0.0)",
                hovermode="closest",
                margin=dict(b=40, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            ),
        )

        if display:
            fig.show()
        else:
            fig.write_image("co-citation-graph.png", scale=2, width=1980, height=1200)

    def filter_low_co_citations(self, criteria: int) -> None:
        """
        Remove low weight edges and isolated nodes

        Args:
            criteria (int): The weight minimum in the resulting graph
        """
        self.co_citation_graph.remove_edges_from(
            [
                e[:2]
                for e in list(
                    filter(
                        lambda e: e[2]["weight"] < criteria,
                        self.co_citation_graph.edges(data=True),
                    )
                )
            ]
        )
        self.co_citation_graph.remove_nodes_from(
            list(nx.isolates(self.co_citation_graph))
        )

    def filter_low_co_citations_nodes(self, criteria: int) -> None:
        """
        Remove low weight nodes

        Args:
            criteria (int): The weight minimum in the resulting graph
        """
        self.co_citation_graph.remove_nodes_from(
            [
                n[0]
                for n in list(
                    filter(
                        lambda n: n[1]["weight"] < criteria,
                        self.co_citation_graph.nodes(data=True),
                    )
                )
            ]
        )

    def write_graph_edges(self, filename: str) -> None:
        """
        Write the edge list to a file

        Args:
            filename (str): The path to the file
        """
        nx.write_weighted_edgelist(
            self.co_citation_graph, filename, "utf-8", delimiter="\t"
        )
