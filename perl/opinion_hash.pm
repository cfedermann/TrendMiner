package opinion_hash;

$VERSION = '0.55';
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(%polarity_it);

%polarity_it = (
		"abuso" => {
			    POL => "0",
			   },
		"accusato" => {
			       POL => "0",
			      },
		"affari" => {
			     POL => "0",
			    },
		"affonda" => {
			      POL => "0",
			     },
		"allunga" => {
			      POL => "0",
			     },
		"altalena" => {
			       POL => "0",
			      },
		"arresto" => {
			      POL => "0",
			     },
		"azzeramento" => {
				  POL => "0",
				 },
		"bancarotta" => {
				 POL => "0",
				},
		"bene" => {
			   POL => "3",
			  },
		"bond" => {
			   POL => "3",
			  },
		"boomerang" => {
				POL => "1",
			       },
		"bufera" => {
			     POL => "0",
			    },
		"buon" => {
			   POL => "3",
			  },
		"buona" => {
			     POL => "3",
			    },
		"cade" => {
			   POL => "0",
			  },
		"carcere" => {
			      POL => "0",
			     },
		"cartolarizzano" => {
				     POL => "3",
				    },
		"cartolarizzazioni" => {
					POL => "3",
				       },
		"caso" => {
			   POL => "1",
			  },
		"cautelare" => {
				POL => "0",
			       },
		"cede" => {
			   POL => "1",
			  },
		"custodia" => {
			       POL => "0",
			      },
		"coda" => {
			   POL => "0",
			  },
		"coinvolgimento" => {
				     POL => "0",
				    },
		"colpevole" => {
				POL => "0",
			       },
		"complessi" => {
				POL => "1",
			       },
		"conflitto" => {
				POL => "1",
			       },
		"congelata" => {
				POL => "1",
			       },
		"correre" => {
				POL => "3",
			       },
		"crack" => {
			    POL => "0",
			   },
		"cresecere" => {
				POL => "3",
			       },
		"crisi" => {
			    POL => "0",
			   },
		"debole" => {
			    POL => "1",
			   },
		"debut" => {
			    POL => "3",
			   },
		"debutto" => {
			      POL => "3",
			     },
		"debuttano" => {
				POL => "3",
			       },
		"deterioramento" => {
				POL => "0",
			       },
		"difficoltá" => {
				 POL => "1",
				},
		"difficili" => {
				POL => "1",
			       },
		"danni" => {
			    POL => "0",
			   },
		"dimissioni" => {
				 POL => "0",
				},
		"disguidi" => {
			       POL => "1",
			      },
		"escalation" => {
				 POL => "0",
				},
		"festeggia" => {
				POL => "4",
			       },
		"fuor" => {
			   POL => "0",
			  },
		"guadagni" => {
			       POL => "4",
			      },
		"giudiziaria" => {
				  POL => "1",
				 },
		"imporre" => {
			      POL => "1",
			     },
		"ispezione" => {
				POL => "0",
			       },
		"inesigibili" => {
				  POL => "0",
				 },
		"inchieste" => {
				POL => "0",
			       },
		"ko" => {
    				POL => "0",
      			},
		"leader" => {
			     POL => "4",
			    },
		"leadership" => {
				 POL => "4",
				},
		"mancato" => {
			      POL => "1",
			     },
		"massimo" => {
			      POL => "4",
			     },
		"massima" => {
			      POL => "4",
			     },
		"ok" => {
			 POL => "3",
			},
		"operazion" => {
				POL => "3",
			       },
		"obbligazioni" => {
				   POL => "3",
				  },
		"perdita" => {
			       POL => "1",
			      },
		"perdite" => {
			       POL => "1",
			      },
		"positiva" => {
			       POL => "3",
			      },
		"positivo" => {
			       POL => "3",
			      },
		"rosso" => {
			       POL => "1",
			      },
		"securiti" => {
			       POL => "3",
			      },
		"premiata" => {
			    POL => "3",
			   },
		"premiato" => {
			    POL => "3",
			   },
		"pront" => {
			    POL => "3",
			   },
		"scandolo" => {
			       POL => "0",
			      },
		"scendere" => {
			       POL => "1",
			      },
		"scintille" => {
				POL => "4",
			       },
		"pericoli" => {
			       POL => "1",
			      },
		"salita" => {
			     POL => "4",
			    },
		"svetta" => {
			     POL => "4",
			    },
		"sveta" => {
			     POL => "4",
			    },
		"risolti" => {
			      POL => "1",
			     },
		"inchiesta" => {
				POL => "0",
			       },
		"fallimento" => {
				 POL => "0",
				},
		"pressione" => {
				POL => "0",
			       },
		"felicemente" => {
				  POL => "3",
				 },
		"spericolat" => {
				 POL => "0",
				},
		"incautamente" => {
				   POL => "1",
				  },
		"boccia" => {
			     POL => "0",
			    },
		"irregolaritá" => {
				   POL => "0",
				  },
		"attrice" => {
			      POL => "4",
			     },
		"truffa" => {
			     POL => "0",
			    },
		"contratti-truffa" => {
				       POL => "0",
				      },
		"monitorata" => {
				 POL => "1",				 
				},
		"piace" => {
				 POL => "3",				 
				},
		"plusvalenza" => {
				  POL => "3",
				 },
		"successo" => {
			       POL => "4",
			      },
		"sindrome" => {
			       POL => "0",
			      },
		"molto" => {
			    POL => "3",
			   },
		"favorevole" => {
				 POL => "3",
				},
		"attivo" => {
			     POL => "3",
			    },
		"sbarazzarsi" => {
				  POL => "0",
				 },
		"crolla" => {
			     POL => "0",
			    },
		"riscriva" => {
			       POL => "1",
			      },
		"onere" => {
			    POL => "0",
			   },
		"arrestato" => {
				POL => "0",
			       },
		"beffa" => {
			    POL => "0",
			   },
		"mancato" => {
			      POL => "1",
			     },
		"problema" => {
			       POL => "0",
			      },
		"instabilitá" => {
				  POL => "0",
				 },
		"coinvolgimento" => {
				     POL => "0",
				    },
		"junk" => {
			   POL => "0",
			  },
		"migliorato" => {
				 POL => "3",
				},
		"disdetta" => {
			       POL => "1",
			      },
		"scivola" => {
			      POL => "0",
			     },
		"solida" => {
			     POL => "3",
			    },
		"scivolone" => {
				POL => "0",
			       },
		"cad" => {
			  POL => "0",
			 },
		"negativo" => {
			       POL => "0",
			      },
		"negativa" => {
			       POL => "0",
			      },
		"chiesto" => {
			      POL => "1",
			     },
		"crisi" => {
			    POL => "0",
			   },
		"colpit" => {
			     POL => "0",
			    },
		"gettonati" => {
				POL => "3",
			       },
		"caso" => {
			   POL => "1",
			  },
		"pressing" => {
			       POL => "1",
			      },
		"malaugurata" => {
				  POL => "0",
				 },
		"penalizzato" => {
				  POL => "1",
				 },
		"migliore" => {
			       POL => "4",
			      },
		"mirino" => {
			     POL => "1",
			    },
		"anomalia" => {
			       POL => "0",
			      },
		"pareggiare" => {
				 POL => "1",
				},
		"pesa" => {
			   POL => "1",
			  },
		"guadagn" => {
			      POL => "3",
			     },
		"elevata" => {
			      POL => "3",
			     },
		"revocato" => {
			       POL => "1",
			      },
		"mancato" => {
			      POL => "1",
			     },
		"oneri" => {
			    POL => "1",
			   },
		"pole position" => {
				    POL => "4",
				   },
		"moltiplicazione" => {
				      POL => "4",
				     },
		"illecitamente" => {
				    POL => "0",
				   },
		"peggiori" => {
			       POL => "0",
			      },
		"crack" => {
			    POL => "0",
			   },
		"crescita" => {
			       POL => "4",
			      },
		"massimi" => {
			      POL => "4",
			     },
		"caso" => {
			   POL => "1",
			  },
		"pieno" => {
			    POL => "4",
			   },
		"richieste" => {
				POL => "4",
			       },
		"severissima" => {
				  POL => "1",
				 },
		"scoppio" => {
			      POL => "1",
			     },
		"dimissionario" => {
				    POL => "0",
				   },
		"dinamismo" => {
				POL => "4",
			       },
		"successo" => {
			       POL => "4",
			      },
		"rosso" => {
			    POL => "0",
			   },
		"sostenuta" => {
				POL => "3",
			       },
		"buco" => {
			   POL => "0",
			  },
		"problemino" => {
				 POL => "0",
				},
		"in bilico" => {
				POL => "0",
			       },
		"redini" => {
			     POL => "1",
			    },
		"performance" => {
				  POL => "3",
				 },
		"riavvio" => {
			      POL => "3",
			     },
		"caduti" => {
			     POL => "0",
			    },
		"azzera" => {
			     POL => "0",
			    },
		"pesante" => {
			      POL => "0",
			     },
		"ingenui" => {
			      POL => "1",
			     },
		"primo" => {
			    POL => "4",
			   },
		"ricognizione" => {
				   POL => "0",
				  },
		"vicissitudini" => {
				    POL => "1",
				   },
		"scandalo" => {
			       POL => "0",
			      },
		"equilibrio" => {
				 POL => "2",
				},
		"rilancio" => {
			       POL => "0",
			      },
		"complica" => {
			       POL => "1",
			      },
		"intercettazioni" => {
				      POL => "1",
				     },
		"pole" => {
			   POL => "4",
			  },
		"questione" => {
				POL => "1",
			       },
		"successo" => {
			       POL => "4",
			      },
		"crescono" => {
			       POL => "4",
			      },
		"esposizioni" => {
				  POL => "1",
				 },
		"valere" => {
			     POL => "3",
			    },
		"ricavi" => {
			     POL => "3",
			    },
		"ricchi" => {
			     POL => "4",
			    },
		"poco" => {
			   POL => "1",
			  },
		"Reat" => {
			   POL => "0",
			  },
		"trauma" => {
			     POL => "0",
			    },
		"inchiesta" => {
				POL => "0",
			       },
		"rialzo" => {
			     POL => "3",
			    },
		"rinnovo" => {
			      POL => "1",
			     },
		"impennare" => {
				POL => "4",
			       },
		"scandalo" => {
			       POL => "0",
			      },
		"sprofonda" => {
				POL => "0",
			       },
		"truffa" => {
			     POL => "0",
			    },
		"prima" => {
			    POL => "4",
			   },
		"nulli" => {
			    POL => "0",
			   },
		"rush" => {
			   POL => "4",
			  },
		"dimissioni" => {
				 POL => "1",
				},
		"impugna" => {
			      POL => "1",
			     },
		"vicenda" => {
			      POL => "1",
			     },
		"dura" => {
			   POL => "0",
			  },
		"frena" => {
			    POL => "0",
			   },
		"deviato" => {
			      POL => "0",
			     },
		" dubbio" => {
			      POL => "1",
			     },
		"distrarre" => {
				POL => "0",
			       },
		"peggior" => {
			      POL => "0",
			     },
		"tensione" => {
			       POL => "0",
			      },
		"tranquilli" => {
				 POL => "3",
				},
		"pericolos" => {
				POL => "1",
			       },
		"tempesta" => {
			       POL => "0",
			      },
		"scossoni" => {
			       POL => "0",
			      },
		"arresto" => {
			      POL => "0",
			     },
		"rafforzarsi" => {
				  POL => "3",
				 },
		"progresso" => {
				POL => "4",
			       },
		"successo" => {
			       POL => "4",
			      },
		"terremoto" => {
				POL => "1",
			       },
		"esposizione" => {
				  POL => "0",
				 },
		"misfatti" => {
			       POL => "0",
			      },
		"azzerata" => {
			       POL => "0",
			      },
		"indagini" => {
			       POL => "0",
			      },
		"indagati" => {
			       POL => "1",
			      },
		"scandalo" => {
			       POL => "0",
			      },
		"spericolato" => {
				  POL => "0",
				 },
		"mina" => {
			   POL => "1",
			  },
		"protagoniste" => {
				   POL => "4",
				  },
		"inchiesta" => {
				POL => "1",
			       },
		"scorsa" => {
			     POL => "0",
			    },
		"scandali" => {
			       POL => "0",
			      },
		"accordo" => {
			      POL => "3",
			     },
		"sovraperformance" => {
				       POL => "4",
				      },
		"in fuga" => {
			      POL => "0",
			     },
		"soluzion" => {
			       POL => "3",
			      },
		"conciliative" => {
				   POL => "3",
				  },
		"aggiotaggio" => {
				  POL => "0",
				 },
		"anomalo" => {
			      POL => "0",
			     },
		"incremento" => {
				 POL => "4",
				},
		"recupera" => {
			       POL => "3",
			      },
		"inquietante" => {
				  POL => "1",
				 },
		"imbarazzo" => {
				POL => "1",
			       },
		"carcere" => {
			      POL => "1",
			     },
		"corsa" => {
			    POL => "0",
			   },
		"giudici" => {
			      POL => "1",
			     },
		"oneroso" => {
			      POL => "1",
			     },
		"tensioni" => {
			       POL => "1",
			      },
		"classifica" => {
				 POL => "4",
				},
		"classifica" => {
				 POL => "4",
				},
#		"fiat" => {
#			   POL => "2",
#			  },
		"rimbalza" => {
			       POL => "4",
			      },
		"positivi" => {
			       POL => "4",
			      },
		"recuperat" => {
				POL => "4",
			       },
		"aumentare" => {
				POL => "3",
			       },
		"tantissimo" => {
				 POL => "4",
				},
		"rialzi" => {
			     POL => "4",
			    },
		"carcere" => {
			      POL => "0",
			     },
		"tappeto" => {
			      POL => "0",
			     },
		"frenata" => {
			      POL => "0",
			     },
		"prim" => {
			   POL => "3",
			  },
		"profitti" => {
			       POL => "4",
			      },
		"esplosi" => {
			      POL => "4",
			     },
		"crisi" => {
			    POL => "0",
			   },
		"sospettano" => {
				 POL => "1",
				},
		"riscuotend" => {
				 POL => "3",
				},
		"ridotto" => {
			      POL => "0",
			     },
		"bufera" => {
			     POL => "0",
			    },
		"brillano" => {
			       POL => "4",
			      },
		"tensione" => {
			       POL => "0",
			      },
		"minaccia" => {
			       POL => "0",
			      },
		"bussa" => {
			    POL => "1",
			   },
		"fort" => {
			   POL => "3",
			  },
		"perdite" => {
			      POL => "0",
			     },
		"preferite" => {
				POL => "3",
			       },
		"crollato" => {
			       POL => "0",
			      },
		"intoppo" => {
			      POL => "0",
			     },
		"rottura" => {
			      POL => "1",
			     },
		"dimissioni" => {
				 POL => "1",
				},
		"delinquere" => {
				 POL => "0",
				},
		"lite" => {
			   POL => "0",
			  },
		"liti" => {
			   POL => "0",
			  },
		"incrociate" => {
				 POL => "0",
				},
		"deposizione" => {
				  POL => "0",
				 },
		"esplode" => {
			      POL => "0",
			     },
		"crollo" => {
			     POL => "0",
			    },
		"zero" => {
			   POL => "0",
			  },
		"tolleranza" => {
				 POL => "3",
				},
		"perso" => {
			    POL => "0",
			   },
		"record" => {
			     POL => "4",
			    },
		"volo" => {
			   POL => "4",
			  },
		"peggior" => {
			      POL => "1",
			     },
		"dimission" => {
				POL => "1",
			       },
		"affare" => {
			     POL => "1",
			    },
		"incremento" => {
				 POL => "4",
				},
		"perde" => {
			    POL => "1",
			   },
		"precipitare" => {
				  POL => "0",
				 },
		"abbassa" => {
			      POL => "1",
			     },
#		"utile" => {
#			    POL => "3",
#			   },
		"perdita" => {
			      POL => "0",
			     },
		"manipol" => {
			      POL => "1",
			     },
		"danneggiato" => {
				  POL => "0",
				 },
		"mirino" => {
			     POL => "1",
			    },
		"DANNI" => {
			    POL => "0",
			   },
		"nera" => {
			   POL => "0",
			  },
		"beneficiato" => {
				  POL => "3",
				 },
		"fallimento" => {
				 POL => "0",
				},
		"mancata" => {
			      POL => "0",
			     },
		"ripari" => {
			     POL => "1",
			    },
		"chiede" => {
			     POL => "1",
			    },
		"outperform" => {
				POL => "3",
			       },

		"profittevole" => {
				   POL => "3",
				  },
		"attacco" => {
			      POL => "1",
			     },
		"recupero" => {
			       POL => "3",
			      },
		"sopravvissuta" => {
				    POL => "1",
				   },
		"quintuplicato" => {
				    POL => "4",
				   },
		"quotazioni" => {
				 POL => "4",
				},
		"reat" => {
			    POL => "0",
			   },
		"plusvalenze" => {
				  POL => "4",
				 },
		"cresc" => {
			    POL => "4",
			   },
		"massim" => {
			     POL => "4",
			    },
		"negativ" => {
			      POL => "0",
			     },
		"incidente" => {
				POL => "0",
			       },
		"boom" => {
			   POL => "4",
			  },
		"raddoppi" => {
			       POL => "3",
			      },
		"colpit" => {
			     POL => "0",
			    },
		"coinvolt" => {
			       POL => "0",
			      },
		"recupero" => {
			       POL => "3",
			      },
		"decolla" => {
			      POL => "4",
			     },
		"redditività" => {
				  POL => "3",
				 },
		"sufficiente" => {
				  POL => "1",
				 },
		"increment" => {
				POL => "3",
			       },
		"sold" => {
			   POL => "0",
			  },
		"recess" => {
			     POL => "1",
			    },
		"tempesta" => {
			       POL => "0",
			      },
		"scaricat" => {
			       POL => "0",
			      },
		"crollo" => {
			      POL => "0",
			     },
		"stabilizzazione" => {
				      POL => "3",
				     },
		"chiude" => {
			     POL => "2",
			    },
		"sostenuto" => {
				POL => "3",
			       },
		"arrest" => {
			     POL => "0",
			    },
		"interrogator" => {
				   POL => "0",
				  },
		"malversazion" => {
				   POL => "0",
				  },
		"conferm" => {
			      POL => "3",
			     },
		"acceler" => {
			      POL => "4",
			     },
		"timore" => {
			     POL => "0",
			    },
		"piu" => {
			  POL => "4",
			 },
		"esposizione" => {
				  POL => "0",
				 },
		"fulminante" => {
				 POL => "4",
				},
		"clamorosi" => {
				POL => "0",
			       },
		"problemi" => {
			       POL => "1",
			      },
		"profitt" => {
			      POL => "4",
			     },
		"rallentato" => {
				 POL => "1",
				},
		"aumento" => {
			      POL => "3",
			     },
		"querele" => {
			      POL => "1",
			     },
		"benefici" => {
			       POL => "3",
			      },
		"teme" => {
			   POL => "1",
			  },
		"risarcimento" => {
				   POL => "1",
				  },
		"perdit" => {
			     POL => "0",
			    },
		"eclatanti" => {
		
				POL => "0",
			       },
		"interessante" => {
				   POL => "3",
				  },
		"dossier" => {
			      POL => "0",
			     },
		"crolla" => {
			     POL => "0",
			    },
		"pesant" => {
			     POL => "1",
			    },
		"carcere" => {
			      POL => "0",
			     },
		"migliore" => {
			       POL => "4",
			      },
		"fiduciae" => {
			       POL => "4",
			      },
		"disavventure" => {
				   POL => "1",
				  },
		"oscillazioni" => {
				   POL => "1",
				  },
		"ampie" => {
			    POL => "3",
			   },
		"scandali" => {
			       POL => "0",
			      },
		"difficoltá" => {
				 POL => "1",
				},
		"perdite" => {
			      POL => "0",
			     },
		"enorm" => {
			    POL => "3",
			   },
		"nuova" => {
			    POL => "3",
			   },
		"valore" => {
			     POL => "4",
			    },
		"profitti" => {
			       POL => "3",
			      },
		"fuga" => {
			   POL => "0",
			  },
		"inchiesta" => {
				POL => "0",
			       },
		"voragine" => {
			       POL => "0",
			      },
		"ciclone" => {
			      POL => "0",
			     },
		"balzo" => {
			    POL => "4",
			   },
		"minim" => {
			    POL => "0",
			   },
		"crescita" => {
			       POL => "3",
			      },
		"successo" => {
			       POL => "4",
			      },
		"recupera" => {
			       POL => "3",
			      },
		"volo" => {
			   POL => "4",
			  },
		"anomalie" => {
			       POL => "0",
			      },
		"danno" => {
			    POL => "0",
			   },
		"pesan" => {
			    POL => "1",
			   },
		"timor" => {
			    POL => "1",
			   },
		"maxi" => {
			   POL => "3",
			  },
		"top five" => {
			       POL => "4",
			      },
		"ennesim" => {
			      POL => "1",
			     },
		"tegola" => {
			     POL => "0",
			    },
		"ferm" => {
			   POL => "1",
			  },
		"trasparent" => {
				 POL => "3",
				},
		"solide" => {
			     POL => "3",
			    },
		"prima" => {
			    POL => "4",
			   },
		"taglio" => {
			     POL => "3",
			    },
		"indagat" => {
			      POL => "0",
			     },
		"nefast" => {
			     POL => "0",
			    },
		"svalutazione" => {
				   POL => "0",
				  },
		"difficoltá" => {
				 POL => "0",
				},
		"turbolente" => {
				 POL => "0",
				},
		"timori" => {
			    POL => "0",
			   },
		"cediment" => {
			       POL => "0",
			      },
		"ipotesi di reato" => {
				       POL => "1",
				      },
		"indagati dalla procura di Roma" => {
						     POL => "0",
						    },
		"recuperato" => {
				 POL => "3",
				},
		"in pressing" => {
				  POL => "0",
				 },
		"festeggia i guadagni" => {
					   POL => "4",
					  },
		"perdite" => {
			      POL => "0",
			     },
		"carcere di Regina Coeli scende il campo il senatore Francesco Cossiga, colui che #; come raccontato ieri dal detenuto stesso #; presenzió alla cresima del finanziere coinvolto nello scandalo" => {
																										     POL => "0",
																										    },
		"largheggiato" => {
				   POL => "1",
				  },
		"crisi della finanza strutturata, innescata dalla bolla dei mutui subprime Usa, e le ricadute" => {
														   POL => "0",
														  },
		"rialzo" => {
			     POL => "4",
			    },
		"avversario dichiarato: chi di volta in volta non gestisce le banche in modo sano e prudente; chi tradisce" => {
																POL => "0",
															       },
		"garanzia sullo stato patrimoniale" => {
							POL => "3",
						       },
		"perdite nette" => {
				    POL => "0",
				   },
		"fa il pieno" => {
				  POL => "4",
				 },
		"vicenda della Banca Italease che ha pagato la perdita della reputazione" => {
											      POL => "1",
											     },
		"fortunati" => {
				POL => "3",
			       },
		"garanzia" => {
			       POL => "3",
			      },
		"recupero" => {
			       POL => "3",
			      },
		"arrestato ieri a Milano con altri due ex manager e due intermediari per associazione a delinquere e appropriazione indebita" => {
																		  POL => "0",
																		 },
		"potenzialitá" => {
				   POL => "3",
				  },
		"perdite" => {
			      POL => "4",
			     },
		"invalidi" => {
			       POL => "0",
			      },
		"cbollate" => {
			       POL => "0",
			      },
		"caso" => {
			   POL => "1",
			  },
		"calo" => {
			   POL => "0",
			  },
		"non c'era" => {
				POL => "1",
			       },
		"scottante" => {
				POL => "1",
			       },
		"perdono" => {
			      POL => "0",
			     },
		"dossier" => {
			      POL => "1",
			     },
		"calo" => {
			   POL => "0",
			  },
		"boomerang" => {
				POL => "1",
			       },
		"impennata" => {
				POL => "4",
			       },
		"costi" => {
			    POL => "1",
			   },
		"dimenticanza" => {
				   POL => "1",
				  },
		"truffati" => {
			       POL => "0",
			      },
		"incertezza" => {
				 POL => "1",
				},
		"ribasso" => {
			      POL => "0",
			     },
		"giudiziarie" => {
				  POL => "0",
				 },
		"escalation" => {
				 POL => "0",
				},
		"drammatica" => {
				 POL => "0",
				},
		"crisi" => {
			    POL => "0",
			   },
		"spinge" => {
			     POL => "3",
			    },
		"miglior" => {
			      POL => "4",
			     },
		"strano" => {
			     POL => "1",
			    },
		"spregiudicatezza" => {
					POL => "0",
				       },
		"mostruoso" => {
				POL => "0",
			       },
		"espozione" => {
				POL => "1",
			       },
		"riassetto" => {
				POL => "1",
			       },
		"ribasso" => {
				POL => "1",
			       },
		"ritirato" => {
			       POL => "0",
			      },
		"rovente" => {
			      POL => "0",
			     },
		"indagini" => {
			       POL => "0",
			      },
		"scende" => {
				POL => "1",
			       },
		"scorsa" => {
			     POL => "0",
			    },
		"spettr" => {
			     POL => "0",
			    },
		"non" => {
			  POL => "0",
			 },
		"temer" => {
			    POL => "0",
			   },
		"underperform" => {
				POL => "1",
			       },
		"vola" => {
			   POL => "4",
			  },
	       );

