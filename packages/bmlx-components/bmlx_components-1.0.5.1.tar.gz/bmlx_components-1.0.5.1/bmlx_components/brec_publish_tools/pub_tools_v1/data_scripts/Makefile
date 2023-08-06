version = 1.0.0

deb_dir = dist

all: createdeb
	make clean

builddir:
	mkdir -p $(deb_dir)/usr/local/bin
	cp -rf emb-index.sh update_resource_v3.py update_resource_k8s.py hdfs_helper.py check_model.py sg_hdfs_conf hk_hdfs_conf tools $(deb_dir)/usr/local/bin

createdeb: builddir
	dpkg -b $(deb_dir) cetos_datascript_$(version)_amd64.deb

clean:
	rm -rf $(deb_dir)/usr/local/bin/*

uploadHK:
	hadoop --config hk_hdfs_conf fs -put -f hdfs_helper.py update_resource_v3.py update_resource_k8s.py tools check_model.py sg_hdfs_conf hk_hdfs_conf clean_local_hdfs emb-index.sh __init__.py hdfs://bigocluster/recommend/data_scripts

uploadSG:
	hadoop --config sg_hdfs_conf fs -put -f hdfs_helper.py update_resource_v3.py update_resource_k8s.py tools check_model.py sg_hdfs_conf hk_hdfs_conf clean_local_hdfs emb-index.sh __init__.py hdfs://bigocluster/recommend/data_scripts
