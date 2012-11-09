@nachfiles = glob ("*.xml");

#@nachfiles = glob ("RR2009042291142-borsa.xml");
#@nachfiles = glob ("RR2009040216128449-new.xml");
#@nachfiles = glob ("RR2009041511680480-oggi(ALR).xml");
#@nachfiles = glob ("RR2009050693856-borsa.xml");

use opinion_hash qw (%polarity_it);

%opinion = %opinion_hash::polarity_it;

use input_entity_hash qw (%hash_entity);
%input_hash = %input_entity_hash::hash_entity;

open (XML, ">om.xml") ||
  die "cannot create om-quant.txt: !\n";

open (POLARITYSTRING, ">pol_string.txt") ||
  die "cannot create om-quant.txt: !\n";

#open (TEST, ">text.txt") ||
#  die "cannot create test.txt: !\n";

$file_nr = 1;

$notal_corpus = 0;
$pol_title = 0;
$i = 0;
$j = 0;
$n = 1;
$pol_total = 0;
$string_total = "";
$flag = "false";

foreach $file (@nachfiles) { 
  $/ = "<\/item>";
  $flag = "false";
  $apertura = "false";
  $oggi = "false";
  $stock = "";
  #  $/ = "/rootdoc";
#    print STDERR "\nProcessing $file..............\n";
  open (SOLENACHRICHT, $file) ||
    die "couldn't open $file for reading: $!\n";
  $ntitle = 0;
  $nsummary = 0;
  $ncocchiello = 0; 
  $nint_index = 0;
  $ntext = 0;
  $ntotal_file = 0;
  foreach $line (<SOLENACHRICHT>) {
    $line =~ s/\n//gi;
    $line =~ s/&egrave\;/\é/gi;
    $line =~ s/&ograve\;/\ó/gi;
    $line =~ s/&igrave\;/\í/gi;
    $line =~ s/&ugrave\;/\ú/gi;
    $line =~ s/&agrave\;/\á/gi;
    $line =~ s/&laquo\;/\"/gi;
    $line =~ s/&raquo\;/\"/gi;
    $line =~ s/&quot\;/\'/gi;
    $line =~ s/&eacute\;/è/gi;
    $line =~ s/&Ouml\;/ö/gi;
    $line =~ s/1(&amp\;)?\&deg\;/1/gi;
    $line =~ s/\&euro\;/EURO/gi;
    $line =~ s/\&ndash/\#/gi;
    $line =~ s/\&nbsp/\\t/gi;
    $line =~ s/(\&amp\;)?egrave\;/\é/gi;
    $line =~ s/(\&amp\;)?ograve\;/\ó/gi;
    $line =~ s/(\&amp\;)?igrave\;/\í/gi;
    $line =~ s/(\&amp\;)?ugrave\;/\ú/gi;
    $line =~ s/(\&amp\;)?agrave\;/\á/gi;
    $line =~ s/(\&amp\;)?laquo\;/\"/gi;
    $line =~ s/(\&amp\;)?raquo\;/\"/gi;
    $line =~ s/(\&amp\;)?quot\;/\'/gi;
    $line =~ s/(\&amp\;)?eacute\;/è/gi;
    $line =~ s/(\&amp\;)?Ouml\;/ö/gi;
    $line =~ s/1(&amp\;)?deg\;/1/gi;
    $line =~ s/(\&amp\;)?euro\;/EURO/gi;
    $line =~ s/(\&amp\;)?ndash/\#/gi;
    $line =~ s/(\&amp\;)?nbsp/\\t/gi;
    $line =~ s/'/' /g;
    $line =~ s/"//g;
    if ($line =~/<testata>(.*?)<\/testata>/i) {
      $source = $1;
    } 
    if ($line =~ /<identificativo>(.*?)<\/identificativo>/i) {
      $id = $1;
    } 
    if ($line =~ /<giorno>(.*?)<\/giorno>/i) {
      $day_of_week = $1;
    }
    if ($line =~ /<data>(.*?)<\/data>/i) {
      #	$key = $1;
      $date = $1;
      $date =~ s/(\d+)(\/|\-)//;
      $year = $1;
      $date =~ s/(\d+)(\/|\-)//;
      $month = $1;
      $date =~ s/(\d+)//;
      $day = $1;
    }
    if ($source =~ /sole/i) { 
      foreach $string (sort{length($a) cmp length($b)} keys %input_hash) {
	$name = $string;    
	$entity = $input_hash{$name}{REF};
	if ($line =~ /<TITOLO>(.*)<\/TITOLO>/) {
	  $title = $1;
	  $title =~ s/\~\#\#p//g;
	  $title =~ s/<\/titolo>//gi;
	  $title =~ s/<\!\[CDATA\[//gi;
	  $title =~ s/~\#\#02//gi;
	  $title =~ s/~\#\#00//gi;
	  $title =~ s/\]\]>//g;
	  $title =~ s/-2-//g;
	  #      $title =~ s/C[0-9A-Z]+//g;
	  if ($title =~ /\b$name/i) {
	    $om{$entity}{$file}{pubdate}{year} = $year;
	    $om{$entity}{$file}{pubdate}{month} = $month;
	    $om{$entity}{$file}{pubdate}{day} = $day;
	    $om{$entity}{$file}{source} = $source;
	    $om{$entity}{$file}{id} = $id;
	    $om{$entity}{$file}{pubdate}{dofw} = $day_of_week;
	    $om{$entity}{$file}{title} = $title;
	    @title = split(/,/,$title);
	    foreach $phrase (@title) {
	      if ($phrase =~ /\b$name/i ) {
		$phrase = lc($phrase);
		@subphrase = split(/ /,$phrase);
		foreach $item (@subphrase) {
		  #  $item =~ s/\,//;
		  $item = lc($item);
		  $om{$entity}{$file}{title}{$j}{string} = $phrase;
		  #	  $item = substr($item,0);
		  if (defined $opinion{$item}) {
		    $om{$entity}{$file}{title}{$j}{polarity} = $opinion{$item}{POL}; 
		    $flag = $true;
		  } 
		}
	      }
	      if ($flag eq "false") {
		$om{$entity}{$file}{title}{$j}{polarity} = "2";
	      }
	      $j++;
	      $flag = "false";
	    }
	    $j = 0;
	  }
	}
	if ($line =~ /<sommario>(.*)<\/sommario>/i) {
	  $summary = $1;
	  $summary =~ s/\~\#\#p//g;
	  $summary =~ s/<\/sommario>//g;
	  $summary =~ s/<\!\[CDATA\[//g;
	  $summary =~ s/~\#\#02//g;
	  $summary =~ s/~\#\#00//g;
	  $summary =~ s/\]\]>//g;
	  #      $summary =~ s/C[0-9A-Z]+//g;
	  if ($summary =~ /\b$name/i) {
	    $om{$entity}{$file}{pubdate}{year} = $year;
	    $om{$entity}{$file}{pubdate}{month} = $month;
	    $om{$entity}{$file}{pubdate}{day} = $day;
	    $om{$entity}{$file}{source} = $source;
	    $om{$entity}{$file}{id} = $id;
	    $om{$entity}{$file}{pubdate}{dofw} = $day_of_week;
	    $om{$entity}{$file}{summary} = $summary;
	    #	    $nsummary++;
	    #         	  $ntotal_file = $ntotal_file + $nsummary;
	    @summary = (/ - /,$summary);
	    foreach $phrase (@summary) {
	      if ($phrase =~ /\b$name/i ) {
		$phrase = lc($phrase);
		@subphrase = split(/ /,$phrase);
		foreach $item (@subphrase) {
		  #  $item =~ s/\,//;
		  $item = lc($item);
		  $om{$entity}{$file}{summary}{$j}{string} = $phrase;
		  #	  $item = substr($item,0);
		  if (defined $opinion{$item}) {
		    $om{$entity}{$file}{summary}{$j}{polarity} = $opinion{$item}{POL}; 
		    $flag = $true;
		  } 
		}
	      }
	      if ($flag eq "false") {
		$om{$entity}{$file}{summary}{$j}{polarity} = "2";
	      }
	      $j++;
	      $flag = "false";
	    }
	    $j = 0;
	  }
	}
	if ($line =~ /<occhiello>(.*)<\/occhiello>/i) {
	  $int_index = $1;
	  $int_index =~ s/\~\#\#p//g;
	  $int_index =~ s/<\/occhiello>//g;
	  $int_index =~ s/<\!\[CDATA\[//g;
	  $int_index =~ s/~\#\#02//g;
	  $int_index =~ s/~\#\#00//g;
	  $int_index =~ s/\]\]>//g;
	  #      	#      $int_index =~ s/C[0-9A-Z]+//g;
	  if ($int_index =~ /\b$name/i) {
	    $om{$entity}{$file}{pubdate}{year} = $year;
	    $om{$entity}{$file}{pubdate}{month} = $month;
	    $om{$entity}{$file}{pubdate}{day} = $day;
	    $om{$entity}{$file}{source} = $source;
	    $om{$entity}{$file}{id} = $id;
	    $om{$entity}{$file}{pubdate}{dofw} = $day_of_week;
	    $om{$entity}{$file}{int_index} = $int_index;
	    #      	  $nint_index++;
	    #      	  $ntotal_file = $ntotal_file + $nint_index;
	    @int_index = (/ - /,$int_index);
	    foreach $phrase (@int_index) {
	      if ($phrase =~ /\b$name/i ) {
		$phrase = lc($phrase);
		@subphrase = split(/ /,$phrase);
		foreach $item (@subphrase) {
		  #  $item =~ s/\,//;
		  $item = lc($item);
		  $om{$entity}{$file}{int_index}{$j}{string} = $phrase;
		  #	  $item = substr($item,0);
		  if (defined $opinion{$item}) {
		    $om{$entity}{$file}{int_index}{$j}{polarity} = $opinion{$item}{POL}; 
		    $flag = $true;
		  } 
		}
	      }
	      if ($flag eq "false") {
		$om{$entity}{$file}{int_index}{$j}{polarity} = "2";
	      }
	      $j++;
	      $flag = "false";
	    }
	    $j = 0;
	  }
	}
      }
    }
    #       if ($line =~ /<testo>(.+)<\/testo>/i) {
    # 	$body = $1;
    # 	$body =~ s/\~\#\#p//g;
    # 	$body =~ s/<\/TEXT>//g;
    # 	$body =~ s/<\!\[CDATA\[//g;
    # 	$body =~ s/~\#\#02//g;
    # 	$body =~ s/~\#\#00//g;
    # 	$body =~ s/\]\]>//g;
    # 	$body =~ s/<\/testo>//g;
    # 	$body =~ s/<testo>//g;
    # 	$body =~ s/\<b\>//g;
    # 	$body =~ s/\<\/b\>//g;
    # 	#      $body =~ s/C[0-9A-Z]+//g;

    # 	if ($body =~ /\b$name/i) {
    # 	  $om{$entity}{$file}{pubdate}{year} = $year;
    # 	  $om{$entity}{$file}{pubdate}{month} = $month;
    # 	  $om{$entity}{$file}{pubdate}{day} = $day;
    # 	  $om{$entity}{$file}{source} = $source;
    # 	  $om{$entity}{$file}{id} = $id;
    # 	  $om{$entity}{$file}{pubdate}{dofw} = $day_of_week;
    # 	  #	  $om{$entity}{$file}{title}{string} = $title;       
    # 	  #	  $om{$entity}{$file}{body}{string} = $body;       
    # 	  #      $flag = 1;
    # 	  @chapters = split(/BR/, $body);
    # 	  foreach $chap (@chapters) {
    # 	    if ($chap =~ /\b$name/) {
    # 	      @sentences = split(/\; /,$chap);
    # 	      foreach $sent (@sentences) {
    # 		$flag = "false";
    # 		if ($sent =~ /\b$name/i) {
    # 		  @text = split(/ /,$sent);
    # 		  foreach $item (@text) { 
    # 		    #		      $item =~ s/([a-z])/$1 $2/;
    # 		    $item = lc($item);
    # 		    if (exists $opinion{$item}) {
    # 		      $j++;
    # 		      $om{$entity}{$file}{sent}{$ntext}{polarity} = $opinion{$item}{POL};
    # 		      $flag = "true";
    # 		      if (($pol == 0) or ($pol == 1)) {
    # 			$pol_neg++;
    # 			$neg = $pol;
    # 		      } else {
    # 			$pol_pos++;
    # 			$poa = $pol;
    # 		      }
    # 		      #			$pol_text = $pol_text + $pol;
    # 		    } else {
    # 		      #			$pol_text = $pol_text + 2;
    # 		    }
    # 		    $om{$entity}{$file}{sent}{$ntext}{string} = $sent;
    # 		    if ($flag eq "false") {
    # 		      $om{$entity}{$file}{sent}{$ntext}{polarity} = 2;
    # 		    }
    # 		  }
    # 		  $ntext++;
    # 		}
    # 	      }
    # 	    }
    # 	  }
    # 	}
    # 	#	  $j = 1;
    # 	$pol_text = 0;
    # 	$pol_pos = 0;
    # 	$pol_neg = 0;
    #       }
    #     } un
    if ($source =~ /radio/i) {
      foreach $string (sort{length($a) cmp length($b)} keys %input_hash) {
	$name = $string;    
	$entity = $input_hash{$name}{REF};
	if ($line =~ /<titolo>(.*)<\/titolo>/) {
	  $title = $1;
	  $title =~ s/\~\#\#p//g;
	  $title =~ s/<\/titolo>//gi;
	  $title =~ s/<\!\[CDATA\[//gi;
	  $title =~ s/~\#\#02//gi;
	  $title =~ s/~\#\#00//gi;
	  $title =~ s/\]\]>//g;
	  $title =~ s/-2-//g;
	  if (($title !~ /PPPapertura\$/) && ($title !~ /PPPandamento\$/) && (($title !~ /PPPOGGI IN BORSA\$/) )) {
	    #      $title =~ s/C[0-9A-Z]+//g;
	    if ($title =~ /\b$name/i) {
	      $om{$entity}{$file}{pubdate}{year} = $year;
	      $om{$entity}{$file}{pubdate}{month} = $month;
	      $om{$entity}{$file}{pubdate}{day} = $day;
	      $om{$entity}{$file}{source} = $source;
	      $om{$entity}{$file}{id} = $id;
	      $om{$entity}{$file}{pubdate}{dofw} = $day_of_week;
	      $om{$entity}{$file}{title}{string} = $title;
	      @title = split(/\./,$title);
	      foreach $phrase (@title) {
		if ($phrase =~ /\b$name/i ) {
		  $phrase = lc($phrase);
		  @subphrase = split(/ /,$phrase);
 		  foreach $item (@subphrase) {
 		    #  $item =~ s/\,//;
 		    $item = lc($item);
 		    #	  $item = substr($item,0);
 		    if (exists $opinion{$item}) {
 		      $om{$entity}{$file}{title}{polarity} = $opinion{$item}{POL}; 
		      $flag = "true";
 		    }     
 		  }
		}
	      }
	      #	      $j = 1;
	      $pol_title = 0;;
	      $pol_pos = 0;
	      $pol_neg = 0;
	      #      $ntotal_corpus = $ntotal_corpus + $ntotal_file;
	    }
	    if ($title =~ /apertura$/) {
	      $apertura = "true";
	      $om{$entity}{$file}{quant}{hour} = "09";
	      $om{$entity}{$file}{quant}{minute} = "00"; $om{$entity}{$file}{pubdate}{year} = $year;
	      $om{$entity}{$file}{pubdate}{month} = $month;
	      $om{$entity}{$file}{pubdate}{day} = $day;
	      $om{$entity}{$file}{source} = $source;
	      $om{$entity}{$file}{id} = $id;
	      $om{$entity}{$file}{pubdate}{dofw} = $day_of_week;
	      $om{$entity}{$file}{title}{string} = $title;
	    } elsif ($title =~ /andamento/) {
	      $andamento = "true";
	      if ($title =~ /ore (\d+),(\d+)/) {
		$om{$entity}{$file}{quant}{hour} = "$1";
		$om{$entity}{$file}{quant}{minute} = "$2"; 
		$om{$entity}{$file}{pubdate}{year} = $year;
		$om{$entity}{$file}{pubdate}{month} = $month;
		$om{$entity}{$file}{pubdate}{day} = $day;
		$om{$entity}{$file}{source} = $source;
		$om{$entity}{$file}{id} = $id;
		$om{$entity}{$file}{pubdate}{dofw} = $day_of_week;
		$om{$entity}{$file}{title}{string} = $title;
	      }
	    } elsif ($title =~ /OGGI IN BORSA/) {
	      $oggi = "true"; 
	      $om{$entity}{$file}{pubdate}{year} = $year;
	      $om{$entity}{$file}{pubdate}{month} = $month;
	      $om{$entity}{$file}{pubdate}{day} = $day;
	      $om{$entity}{$file}{source} = $source;
	      $om{$entity}{$file}{title} = $title;
	      $om{$entity}{$file}{id} = $id;
	      $om{$entity}{$file}{pubdate}{dofw} = $day_of_week;
	      $om{$entity}{$file}{title}{string} = $title;
	    } elsif ($title =~ /\(BIM\)/) {
	      $bim = "true"; 
	      $om{$entity}{$file}{pubdate}{year} = $year;
	      $om{$entity}{$file}{pubdate}{month} = $month;
	      $om{$entity}{$file}{pubdate}{day} = $day;
	      $om{$entity}{$file}{source} = $source;
	      $om{$entity}{$file}{title} = $title;
	      $om{$entity}{$file}{id} = $id;
	      $om{$entity}{$file}{pubdate}{dofw} = $day_of_week;
	      $om{$entity}{$file}{title}{string} = $title;
	    }
	  }
	}
	if ($line =~ /<testo>(.+)<\/testo>/i) {
	  $body = $1;
	  $body =~ s/\~\#\#p//g;
	  $body =~ s/<\/TEXT>//g;
	  $body =~ s/<\!\[CDATA\[//g;
	  $body =~ s/~\#\#02//g;
	  $body =~ s/~\#\#00//g;
	  $body =~ s/\]\]>//g;
	  $body =~ s/<\/testo>//g;
	  $body =~ s/<testo>//g;
	  $body =~ s/\<b\>//g;
	  $body =~ s/\<\/b\>//g;
	  $body =~ s/\'//g;
	  #      $body =~ s/C[0-9A-Z]+//g;$text = $1;
	  if ($body =~ /\b$name/i) {
	    if ($apertura eq "true") {	
	      if ($body =~ /\b$name\s+(\d+\.\d+)\s+(\-?\d+\.\d*)/) {
		$value = $1;
		$diff = $2;
		#		$om{$entity}{$file}{quant}{string} = body;
		$om{$entity}{$file}{quant}{stock} = $value;
		$om{$entity}{$file}{quant}{polarity} = 2;
		$om{$entity}{$file}{quant}{diff} = $diff;
	      }
	    } elsif ($andamento eq "true") {
	      if ($body =~ /ore (\d+),(\d+)/) {
	      }
	      if ($body =~ /\b$name\s+(\d+\.\d+)\s+(\-?\d+\.\d*)/) {
 		$value = $1;
 		$diff = $2;
		#		$om{$entity}{$file}{quant}{string} = body;
 		$om{$entity}{$file}{quant}{stock} = $value;
 		$om{$entity}{$file}{quant}{polarity} = 2;
 		$om{$entity}{$file}{quant}{diff} = $diff;
 	      }
	    } elsif ($oggi eq "true") {
	      if ($body =~ s/\(aggiornamento alle ore (\d+),(\d+)//) {
		$hour = $1;
		$minute = $2;
		$om{$entity}{$file}{pubtime}{hour} = $hour;
		$om{$entity}{$file}{pubtime}{minute} = $minute; 
	      }
	      $body =~ s/\-\- /\-\-/g;
	      $body =~ s/.*\-\-//;
	      $body =~ s/\&lt\;BR\/\&gt\;(\d+),(\d+)/NEWLINE$1,$2/g;
	      #	      $body =~ s/\&lt\;\-\-\/\&gt\;(\d+),(\d+)/NEWLINE$1,$2/g;
	      $body =~ s/ \s+/ /g;	 
	      @chapters = split(/NEWLINE/, $body);
	      foreach $chap (@chapters) {
		$string_chap = $chap;
		if ($chap =~ /\b$name (cede (il|lo|l\'|l))/) {
		  $chap =~ s/$1\s?/\-/;
		} elsif ($chap =~ /\b$name (gi.+ (dell|del)) /) {
		  $chap =~ s/$1\s?/\-/;
		} elsif ($chap =~ /\b$name (in calo (dell|del)\s?)/) {
		  $chap =~ s/$1\s?/\-/;
		} elsif ($chap =~ /([Ii]n calo (dell|del)\s?) /) {
		  $chap =~ s/$1\s?/\-/;
		} elsif ( ( ($chap =~ /\b$name/) && ($chap =~ /(cede (il|lo|l\'|l)\s?)(\d+(,\d+)?\%)/) ) ) {
		  $diff = "-" . $3;
		  $chap =~ s/$1/\-/;
		} elsif ($chap =~ /\b$name (balza (dell|del|al|a) )/) {
		  $chap =~ s/$1/\+/;
		  $chap =~ s/\+\+/\+/;
		} elsif ($chap =~ /\b$name (balzato (dell|del|al|a) )/) {
		  $chap =~ s/$1/\+/;
		  $chap =~ s/\+\+/\+/;
		} elsif ( ( ($chap =~ /\b$name/) && ($chap =~ /(balza (dell|del|al|a)\s?)(\d+(,\d+)?\%)/) ) ) {
		  $diff = "+" . $3;
		  $chap =~ s/$1/\+/;
		  $chap =~ s/\+\+/\+/;
		} 
		if ($chap =~ /\b$name( [A-Za-z]+)? (\(?[\+\-]?\d+(,\d+)?\%\)?)/) {  
		  $diff = $2;
		  $diff =~ s/\(//;
		  $diff =~ s/\)//;
		} elsif ($chap =~ /(\(?[\+\-]?\d+(,\d+)?\%\)?) \b$name/) {  
		  $diff = $1;
		  $diff =~ s/\(//;
		  $diff =~ s/\)//;
		} 
		if (($diff =~ /\d+/) && ($string_chap =~ /[A-Za-z]+/)) {
		  if ($chap =~ s/(\d+),(\d+)//) {
		    $hours = $1;
		    $minutes = $2;
		    $j = $i + 1;
		    $om{$entity}{$file}{reason}{$i}{hour} = $hours;
		    $om{$entity}{$file}{reason}{$i}{minute} = $minutes; 
		  }
		  $chap =~ s/\&lt\;//; 
		  $chap =~ s/\\&gt\;//; 
		  $chap =~ s/BR//g; 
		  $chap =~ s/ \(?[\+\-]?\d+(,\d+)?\%\)?//;
		  $om{$entity}{$file}{reason}{$i}{diff} = $diff;
		  
		  $om{$entity}{$file}{reason}{$i}{string} = $string_chap;
		  if ($om{$entity}{$file}{reason}{$i}{diff} =~ /\+/) {
		    ($pol_diff = $om{$entity}{$file}{reason}{$i}{diff}) =~ s/\+(\d+)(,\d+)?\%/$1/;
		    ($pol_diff2 = $om{$entity}{$file}{reason}{$i}{diff}) =~ s/(\,\d+)?\%/$1/;
		    if ($pol_diff2 =~ s/\+\d+\,// ) {
		    } else {
		      $pol_diff2 = 0;
		    }
		    if ($pol_diff < 1) { 
		      if ($pol_diff2 < 6) {
			$om{$entity}{$file}{reason}{$i}{polarity} = "2";
		      } else {
			$om{$entity}{$file}{reason}{$i}{polarity} = "3";
		      }
		    } elsif ($pol_diff > 3) {
		      #		  print TEST "hallo ich bin chap $chap und diff $pol_diff\n";
		      $om{$entity}{$file}{reason}{$i}{polarity} = "4";
		    } else {
		      $om{$entity}{$file}{reason}{$i}{polarity} = "3";
		    }
		  } elsif ($om{$entity}{$file}{reason}{$i}{diff} =~ /\-/) {
		    ($pol_diff = $om{$entity}{$file}{reason}{$i}{diff}) =~ s/\-(\d+)(,\d+)?\%/$1/;
		    ($pol_diff2 = $om{$entity}{$file}{reason}{$i}{diff}) =~ s/(\,\d+)?\%/$1/;
		    if ($pol_diff2 =~ s/\+\d+\,// ) {
		    } else {
		      $pol_diff2 = 0;
		    }
		    if ($pol_diff < 1) {
		      if ($pol_diff2 < 4) {
			$om{$entity}{$file}{reason}{$i}{polarity} = "2";
		      } else {
			$om{$entity}{$file}{reason}{$i}{polarity} = "1";
		      } 
		    } elsif ($pol_diff > 2) { 
		      #		      print TEST  "hash_diff $om{$entity}{$file}{reason}{$i}{diff}: pol_diff $pol_diff und pol_diff2 $pol_diff2 und name $name\n"; 
		      $om{$entity}{$file}{reason}{$i}{polarity} = "0"; 
		    } else {
		      $om{$entity}{$file}{reason}{$i}{polarity} = "1";
		    }
		  } else {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "2";
		  }
		  #  }
		  #  else {
		  #    $om{$entity}{$file}{reason}{$i}{polarity} = "2";
		  #  }
		  print POLARITYSTRING "Entity: $entity :: String: $om{$entity}{$file}{reason}{$i}{string} :: Opinion: $om{$entity}{$file}{reason}{$i}{polarity}\n";
		  $i++;
		} elsif (($chap =~ /\b$name/) && not exists($om{$entity}{$file}{reason}{$i}{diff})) {
		  $diff = "NN";
		  if ($chap =~ s/^(\d+),(\d+)//) { 
		    $hours = $1;
		    $minutes = $2;
		    $j = $i + 1;
		    $om{$entity}{$file}{reason}{$i}{hour} = $hours;
		    $om{$entity}{$file}{reason}{$i}{minute} = $minutes; 
		  }
		  $chap =~ s/\&lt\;//;
		  $chap =~ s/\/\&gt\;//;   
		  $chap =~ s/BR//g; 
		  $chap =~ s/ \(?[\+\-]?\d+(,\d+)?\%\)?//;
		  $om{$entity}{$file}{reason}{$i}{diff} = "NN";
		  $om{$entity}{$file}{reason}{$i}{string} = $string_chap; 
		  if ( ($chap =~ /([A-Za-z]+) \b$name/) && (exists $opinion{$1}) ) {
		    $item = $1;
		    $om{$entity}{$file}{reason}{$i}{polarity} = $opinion{$item}{POL};
		  } elsif ( ($chap =~ /\b$name ([A-Za-z]+) /) && (exists $opinion{$1}) ) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = $opinion{$item}{POL};
		  } elsif ($chap =~ /da sell a buy/) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "4";
		  } elsif ($chap =~ /da neutral a buy/) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "3";
		  } elsif ($chap =~ /da buy a neutral/) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "1";
		  } elsif ($chap =~ /da buy a sell/) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "0";
		  } elsif ($chap =~ /(promuove|alza|ingresso in buy|grazie a buy|da [A-Za-z]+ buy|consiglia buy|consiglio di buy|conferma buy)/) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "3";
		  } elsif ($chap =~ /(taglia|taglio|ingresso in sell|da [A-Za-z]+ sell|consiglia sell|consiglio di sell|conferma sell|giudizio a sell)/) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "3";
		  } else {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "2";
		  }
		  #		  print TEST "Ich bin chap2 $chap + name $name\n",
		  
		  $i++;
		}
		undef $diff;
	      }
	      $i = 0;
	      # 	      if ($body =~ /\b$name\s+(\d+\.\d+)\s+(\-?\d+\.\d*)/) {
	      # 		$value = $1;
	      # 		$diff = $2;
	      # #		$om{$entity}{$file}{quant}{string} = body;
	      # 		$om{$entity}{$file}{quant}{stock} = $value;
	      # 		$om{$entity}{$file}{quant}{polarity} = 2;
	      # 		$om{$entity}{$file}{quant}{diff} = $diff;
	      # 	      }
	    } elsif ($bim eq "true") {
	      $body =~ s/\-\- /\-\-/g;
	      $body =~ s/.*\-\-//;
	      $body =~ s/\&lt\;BR\/\&gt\;/ /g;
	      $body =~ s/ \s+/ /g;	 
	      #	      $body =~ s/\&lt\;BR\/\&gt\;(\d+),(\d+)/NEWLINE$1,$2/g;
	      #	      $body =~ s/\&lt\;\-\-\/\&gt\;(\d+),(\d+)/NEWLINE$1,$2/g;
	      @chapters = split(/\. /, $body);
	      foreach $chap (@chapters) {
		$string_chap = $chap;
		if ( $chap =~ /$name/ ) {
		  if ($chap =~ /\b$name (cede (il|lo|l\'|l))/) {
		    $chap =~ s/$1\s?/\-/;
		  } elsif ($chap =~ /\b$name (gi.+ (dell|del)) /) {
		    $chap =~ s/$1\s?/\-/;
		  } elsif ($chap =~ /\b$name (in calo (dell|del)\s?) /) {
		    $chap =~ s/$1\s?/\-/;
		  } elsif ($chap =~ /([Ii]n calo (dell|del)\s?)/) {
		    $chap =~ s/$1\s?/\-/;
		  } elsif ( ( ($chap =~ /\b$name/) && ($chap =~ /(cede (il|lo|l\'|l)\s?)(\d+(,\d+)?\%)/) ) ) {
		    $diff = "-" . $3;
		    $chap =~ s/$1/\-/;
		  } elsif ($chap =~ /\b$name (balza (dell|del|al|a) )/) {
		    $chap =~ s/$1/\+/;
		    $chap =~ s/\+\+/\+/;
		  } elsif ($chap =~ /\b$name (balzato (dell|del|al|a) )/) {
		    $chap =~ s/$1/\+/;
		    $chap =~ s/\+\+/\+/;
		  } elsif ( ( ($chap =~ /\b$name/) && ($chap =~ /(balza (dell|del|al|a)\s?)(\d+(,\d+)?\%)/) ) ) {
		    $diff = "+" . $3;
		    $chap =~ s/$1/\+/;
		    $chap =~ s/\+\+/\+/;
		  }
		  if ($chap =~ /\b$name( [A-Za-z]+)? (\(?[\+\-]?\d+(,\d+)?\%\)?)/) {
		    $diff = $2;
		    $diff =~ s/\(//;
		    $diff =~ s/\)//;
		  } elsif ($chap =~ /(\(?[\+\-]?\d+(,\d+)?\%\)?) \b$name/) {  
		    $diff = $1;
		    $diff =~ s/\(//;
		    $diff =~ s/\)//;
		  } 
		  if (($diff =~ /\d+/) && ($string_chap =~ /[A-Za-z]+/)) {
		    #		  if ($chap =~ s/(\d+),(\d+)//) {
		    #		    $hours = $1;
		    #		    $minutes = $2;
		    #		    $j = $i + 1;
		    #		    $om{$entity}{$file}{reason}{$i}{hour} = $hours;
		    #		    $om{$entity}{$file}{reason}{$i}{minute} = $minutes; 
		    #		  }
		    $chap =~ s/\&lt\;//; 
		    $chap =~ s/\\&gt\;//; 
		    $chap =~ s/BR//g; 
		    $chap =~ s/ \(?[\+\-]?\d+(,\d+)?\%\)?//;
		    $om{$entity}{$file}{reason}{$i}{diff} = $diff;
		    $om{$entity}{$file}{reason}{$i}{string} = $string_chap;
		    if ($om{$entity}{$file}{reason}{$i}{diff} =~ /\+/) {
		      ($pol_diff = $om{$entity}{$file}{reason}{$i}{diff}) =~ s/\+(\d+)(,\d+)?\%/$1/;
		      ($pol_diff2 = $om{$entity}{$file}{reason}{$i}{diff}) =~ s/(\,\d+)?\%/$1/;
		      if ($pol_diff2 =~ s/\+\d+\,// ) {
		      } else {
			$pol_diff2 = 0;
		      }
		      if ($pol_diff < 1) { 
			if ($pol_diff2 < 6) {
			  $om{$entity}{$file}{reason}{$i}{polarity} = "2";
			} else {
			  $om{$entity}{$file}{reason}{$i}{polarity} = "3";
			}
		      } elsif ($pol_diff > 3) {
			#		  print TEST "hallo ich bin chap $chap und diff $pol_diff\n";
			$om{$entity}{$file}{reason}{$i}{polarity} = "4";
		      } else {
			$om{$entity}{$file}{reason}{$i}{polarity} = "3";
		      }
		    } elsif ($om{$entity}{$file}{reason}{$i}{diff} =~ /\-/) {
		      ($pol_diff = $om{$entity}{$file}{reason}{$i}{diff}) =~ s/\-(\d+)(,\d+)?\%/$1/;
		      ($pol_diff2 = $om{$entity}{$file}{reason}{$i}{diff}) =~ s/(\,\d+)?\%/$1/;
		      if ($pol_diff2 =~ s/\+\d+\,// ) {
		      } else {
			$pol_diff2 = 0;
		      }
		      if ($pol_diff < 1) {
			if ($pol_diff2 < 4) {
			  $om{$entity}{$file}{reason}{$i}{polarity} = "2";
			} else {
			  $om{$entity}{$file}{reason}{$i}{polarity} = "1";
			} 
		      } elsif ($pol_diff > 2) { 
			#		      print TEST  "hash_diff $om{$entity}{$file}{reason}{$i}{diff}: pol_diff $pol_diff und pol_diff2 $pol_diff2 und name $name\n"; 
			$om{$entity}{$file}{reason}{$i}{polarity} = "0"; 
		      } else {
			$om{$entity}{$file}{reason}{$i}{polarity} = "1";
		      }
		    } else {
		      $om{$entity}{$file}{reason}{$i}{polarity} = "2";
		    }
		  }  # TD neu
		  $chap =~ s/\&lt\;//;
		  $chap =~ s/\/\&gt\;//;   
		  $chap =~ s/BR//g; 
		  $chap =~ s/ \(?[\+\-]?\d+(,\d+)?\%\)?//;
		  # $om{$entity}{$file}{reason}{$i}{diff} = "NN";
		  $om{$entity}{$file}{reason}{$i}{string} = $string_chap;
		  if ( ($chap =~ /([A-Za-záéí]+) [A-Za-záéí]+\, \b$name/) && (exists $opinion{$1})) {
		    $item = $1;
		    $om{$entity}{$file}{reason}{$i}{polarity} = $opinion{$item}{POL};
		  } elsif ( ($chap =~ /([A-Za-záéí]+) [A-Za-záéí]+ e \b$name/) && (exists $opinion{$1})) {
		    $item = $1;
		    $om{$entity}{$file}{reason}{$i}{polarity} = $opinion{$item}{POL};
		  } elsif ( ($chap =~ /([A-Za-záéí]+) [A-Za-záéí]+\, [A-Za-záéí]+ e \b$name/) && (exists $opinion{$1})) {
		    $item = $1;
		    $om{$entity}{$file}{reason}{$i}{polarity} = $opinion{$item}{POL};
		  } elsif ( ($chap =~ /([A-Za-záéí]+) [A-Za-záéí]+, [A-Za-záéí]+ e \b$name/) && (exists $opinion{$1})) {
		    $item = $1;
		    $om{$entity}{$file}{reason}{$i}{polarity} = $opinion{$item}{POL};
		  } elsif ( ($chap =~ /([A-Za-záéí]+) \b$name/) && (exists $opinion{$1}) ) {
		    $item = $1;
		    $om{$entity}{$file}{reason}{$i}{polarity} = $opinion{$item}{POL};
		  } elsif ( ($chap =~ /\b$name ([A-Za-záéí]+) /) && (exists $opinion{$1}) ) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = $opinion{$item}{POL};
		  } elsif ($chap =~ /da sell a buy/) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "4";
		  } elsif ($chap =~ /da neutral a buy/) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "3";
		  } elsif ($chap =~ /da buy a neutral/) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "1";
		  } elsif ($chap =~ /da buy a sell/) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "0";
		  } elsif ($chap =~ /(promuove|alza|ingresso in buy|grazie a buy|da [A-Za-z]+ buy|consiglia buy|consiglio di buy|conferma buy)/) {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "3";
		    #	    } elsif ($chap =~ /(taglia|taglio|ingresso in sell|da [A-Za-z]+ sell|consiglia sell|consiglio di sell|conferma sell|giudizio a sell)/) {
		    #	      $om{$entity}{$file}{reason}{$i}{polarity} = "3";
		    #	    } else {
		    $om{$entity}{$file}{reason}{$i}{polarity} = "2";
		  }
		  #		  print TEST "Ich bin chap2 $chap + name $name\n",
		  $i++;
	#	}
		if (not defined $diff) {
		  #		    print STDOUT "hallo $name :: $chap \n";
		  $om{$entity}{$file}{reason}{$i}{polarity} = "2";
		  $om{$entity}{$file}{reason}{$i}{string} = $string_chap; 
		}
		undef $diff;
		}
	      }
	    }
	  }
	}
      }
    }
  }
  #  }
  $apertura = "false";
  $andamento = "false";
  $oggi = "false";
  $bim = "false";
  $file_nr++;
}
#}

#print OUT "id\t date\t polarity\t\t\\t text\n";

$i = 0;

$pol_text = "";


print XML "\<\?xml version\=\"1\.0\" encoding\=\"UTF\-8\"\?>\n";
print XML "<opinion>\n";
foreach $ent (sort{$a <=> $b} keys %om) {
  foreach $file (sort{$a <=> $b} keys %{$om{$ent}}) {
    #  if ($entity{$ent}{$file}{ntotal} > 0) {
    if (defined $om{$ent}{$file}{quant}) {
      print QUANT "ent : $ent\n";
      print QUANT "\tsource = $om{$ent}{$file}{source}\n";
      print QUANT "\tid = $om{$ent}{$file}{id}\n";
      print QUANT "\tday = $om{$ent}{$file}{pubdate}{day}\n";
      print QUANT "\tmonth = $om{$ent}{$file}{pubdate}{month}\n";
      print QUANT "\tyear = $om{$ent}{$file}{pubdate}{year}\n";
    } elsif (defined $om{$ent}{$file}{reason}) {
      print REASON "ent : $ent\n";
      print REASON "\tsource = $om{$ent}{$file}{source}\n";
      print REASON "\tid = $om{$ent}{$file}{id}\n";
      print REASON "\tpubdate : day = $om{$ent}{$file}{pubdate}{day}\n";
      print REASON "\tpubdate : month = $om{$ent}{$file}{pubdate}{month}\n";
      print REASON "\tpubdate : year = $om{$ent}{$file}{pubdate}{year}\n";
      print REASON "\tpubtime : hour = $om{$ent}{$file}{reason}{pubtime}{hour}\n";
      print REASON "\tpubtime : minute = $om{$ent}{$file}{reason}{pubtime}{minute}\n";
    } else { 
      print OUT "ent : $ent\n";	
      print OUT "\tdata : source = $om{$ent}{$file}{source}\n";
      print OUT "\tdata : id = $om{$ent}{$file}{id}\n";
      print OUT "\tdata : pubdate : day = $om{$ent}{$file}{pubdate}{day}\n";
      print OUT "\tdata : pubdate : month = $om{$ent}{$file}{pubdate}{month}\n";
      print OUT "\tdata : pubdate : year = $om{$ent}{$file}{pubdate}{year}\n";
    }
    foreach $data (sort{$a <=> $b} keys %{$om{$ent}{$file}} ) {
      if ($data eq 'pubdate') {
	$day = $om{$ent}{$file}{$data}{day};
	$month = $om{$ent}{$file}{$data}{month};
	$year = $om{$ent}{$file}{$data}{year};
      }
      if ($data eq 'source') {
	$source = $om{$ent}{$file}{$data};
	if ($source =~ /sole/i) {
	  print XML "<entity>\n";
	  print XML "<name>$ent<\/name>\n";
	  #  print XML "<mention>";
	  print XML "<source_name>$om{$ent}{$file}{source}<\/source_name>\n";
	  print XML "<source_id>$om{$ent}{$file}{id}<\/source_id>\n";
	  print XML "<source_title>$om{$ent}{$file}{title}<\/source_title>\n";
	  print XML "<pub_date>\n";
	  print XML "<day>$om{$ent}{$file}{pubdate}{day}<\/day>\n";
	  print XML "<month>$om{$ent}{$file}{pubdate}{month}<\/month>\n";
	  print XML "<year>$om{$ent}{$file}{pubdate}{year}<\/year>\n";
	  print XML "<\/pub_date>\n";
	  #	    print XML "<pub_time>\n";
	  #	    print XML "<hour>$om{$ent}{$file}{pubtime}{hour}<\/hour>\n";
	  #	    print XML "<minute>$om{$ent}{$file}{pubtime}{minute}<\/minute>\n";
	  #	    print XML "<\/pub_time>\n";	 
	  foreach $frag (sort{$a <=> $b} keys %{$om{$ent}{$file}{title}}) {
	    print XML "<ticker_string>$om{$ent}{$file}{title}{$frag}{string}<\/ticker_string>\n";   
	    print XML "<polarity>$om{$ent}{$file}{title}{$frag}{polarity}<\/polarity>\n";    
	  } 
	  foreach $frag (sort{$a <=> $b} keys %{$om{$ent}{$file}{summary}}) {
	    print XML "<ticker_string>$om{$ent}{$file}{summary}{$frag}{string}<\/ticker_string>\n";   
	    print XML "<polarity>$om{$ent}{$file}{summary}{$frag}{polarity}<\/polarity>\n";    
	  } 
	  foreach $frag (sort{$a <=> $b} keys %{$om{$ent}{$file}{int_index}}) {
	    print XML "<ticker_string>$om{$ent}{$file}{int_index}{$frag}{string}<\/ticker_string>\n";   
	    print XML "<polarity>$om{$ent}{$file}{int_index}{$frag}{polarity}<\/polarity>\n";    
	  }
	  print XML "<\/entity>\n";
	}
      }
      if ($data eq 'id') {
	$id = $om{$ent}{$file}{$data};
      }
      if ($data eq 'ntotal') {
	print OUT "\tfrequency of naming $om : $om{$ent}{$file}{$data}\n";
      }
      if ($data eq 'title') {
	print OUT "\tdata : $data : string =  $om{$ent}{$file}{$data}{string}\n";
	print OUT "\tdata : $data : polarity = $om{$ent}{$file}{$data}{polarity}\n";
	print OUT "\tdata : $data : polarity_correct = \n";
	print OUT "\tdata : $data : polarity_correct_which_word(s): \n";

	$text = $om{$ent}{$file}{$data}{string};
	$pol = $om{$ent}{$file}{$data}{polarity};
	#	if ($pol <= 4) {
	$pol_total = $pol_total + $pol;
	$string_total = "$string_total" . "\/\/ $text ";  
	#	  print EXC "$ent\t\t$stock\t\t$source\t\t\t$day\.$month\.$year\t\t$pol\t$text\n";
	#	  $n++;
	#	} 
      }
      if ($data eq 'summary') {
	print OUT "\tdata : $data : string =  $om{$ent}{$file}{$data}{string}\n";
	print OUT "\tdata : $data : polarity = $om{$ent}{$file}{$data}{polarity}\n";
	print OUT "\tdata : $data : polarity_correct =  \n";
	print OUT "\tdata : $data : polarity_correct_which_word(s): \n";
	$text = $om{$ent}{$file}{$data}{string};
	$pol = $om{$ent}{$file}{$data}{polarity};
	if ($pol <= 4) {
	  $pol_total = $pol_total + $pol;
	  $string_total = "$string_total" . "\/\/ $text ";  
	  #	  print EXC "$ent\t\t$stock\t\t$source\t\t\t$day\.$month\.$year\t\t$pol\t$text\n";
	  $n++;
	}
      } 
      if ($data eq 'int_index') {
	print OUT "\tdata : $data : string =  $om{$ent}{$file}{$data}{string}\n";
	print OUT "\tdata : $data : polarity = $om{$ent}{$file}{$data}{polarity}\n";
	print OUT "\tdata : $data : polarity_correct =  \n";
	print OUT "\tdata : $data : polarity_correct_which_word(s): \n";
	$text = $om{$ent}{$file}{$data}{string};
	$pol = $om{$ent}{$file}{$data}{polarity};
	if ($pol <= 4) {
	  $pol_total = $pol_total + $pol;
	  $string_total = "$string_total" . "\/\/ $text ";  
	  #	  print EXC "$ent\t\t$stock\t\t$source\t\t\t$day\.$month\.$year\t\t$pol\t$text\n";
	  $n++;
	}
      } 
      if ($data eq 'text') {
	print OUT "\tdata : $data : string = $om{$ent}{$file}{$data}{string}\n";
	print OUT "\tdata : $data : polarity = $om{$ent}{$file}{$data}{polarity}\n";
	print OUT "\tdata : $data : polarity_correct =  \n";
	print OUT "\tdata : $data : polarity_correct_which_word(s): \n";
	$text = $om{$ent}{$file}{$data}{string};
	$pol = $om{$ent}{$file}{$data}{polarity};
	if ($pol <= 4) {
	  $pol_total = $pol_total + $pol;
	  $string_total = "$string_total" . "\/\/ $text ";  
	  #	  print EXC "$ent\t\t$stock\t\t$source\t\t\t$day\.$month\.$year\t\t$pol\t$text\n";
	  $n++;
	}
      }
      if ($data eq 'sent') {
	foreach $sent (sort{$a <=> $b} keys %{$om{$ent}{$file}{sent}}) {
	  print OUT "\tdata : body : string =  $om{$ent}{$file}{$data}{$sent}{string}\n";
	  print OUT "\tdata : body : polarity = $om{$ent}{$file}{$data}{$sent}{polarity}\n";
	  print OUT "\tdata : body : polarity_correct =  \n";
	  print OUT "\tdata : body : polarity_correct_which_word(s): \n";
	  $text = $om{$ent}{$file}{$data}{$sent}{string};
	  $pol = $om{$ent}{$file}{$data}{$sent}{polarity};
	  if ($pol <= 4) {
	    $pol_total = $pol_total + $pol;
	    $string_total = "$string_total" . "\/\/ $text ";
	    #	    print EXC "$ent\t\t$stock\t\t$source\t\t\t$day\.$month\.$year\t\t$pol\t$text\n";
	    $n++;
	  }
	}
      } elsif ( $data eq 'reason' ) {
	print XML "<entity>\n";
	print XML "<name>$ent<\/name>\n";
	#  print XML "<mention>";
	print XML "<source_name>$om{$ent}{$file}{source}<\/source_name>\n";
	print XML "<source_id>$om{$ent}{$file}{id}<\/source_id>\n";
	print XML "<source_title>$om{$ent}{$file}{title}<\/source_title>\n";
	print XML "<pub_date>\n";
	print XML "<day>$om{$ent}{$file}{pubdate}{day}<\/day>\n";
	print XML "<month>$om{$ent}{$file}{pubdate}{month}<\/month>\n";
	print XML "<year>$om{$ent}{$file}{pubdate}{year}<\/year>\n";
	print XML "<\/pub_date>\n";
	print XML "<pub_time>\n";
	print XML "<hour>$om{$ent}{$file}{pubtime}{hour}<\/hour>\n";
	print XML "<minute>$om{$ent}{$file}{pubtime}{minute}<\/minute>\n";
	print XML "<\/pub_time>\n";
	foreach $frag (sort{$a <=> $b} keys %{$om{$ent}{$file}{$data}}) {
	  if (($frag ne 'pubtime') && (defined $om{$ent}{$file}{$data}{$frag}{polarity}) ) {
	    print REASON "\tdiff = $om{$ent}{$file}{$data}{$frag}{diff}\n";
	    print REASON "\treason = $om{$ent}{$file}{$data}{$frag}{string}\n";
	    print REASON "\treason-text-type = \n";
	    print REASON "\treason-text-type-key-words = \n";
	    print REASON "\tticker : hour = $om{$ent}{$file}{$data}{$frag}{hour}\n";
	    print REASON "\tticker : minute = $om{$ent}{$file}{$data}{$frag}{minute}\n";
	    print XML "<ticker_time>\n";
	    print XML "<ticker_hour>$om{$ent}{$file}{reason}{$frag}{hour}<\/ticker_hour>\n";
	    print XML "<ticker_minute>$om{$ent}{$file}{reason}{$frag}{minute}<\/ticker_minute>\n";
	    print XML "<\/ticker_time>\n";
	    print XML "<ticker_string>$om{$ent}{$file}{$data}{$frag}{string}<\/ticker_string>\n";
	    print XML "<polarity>$om{$ent}{$file}{$data}{$frag}{polarity}<\/polarity>\n"; 
	    #	  print XML "<\/entity>\n";	

	    #	print REASON "\tdata : body : quant = $om{$ent}{$file}{$data}{stock}\n";
	    #	print REASON "\tdata : body : diff = $om{$ent}{$file}{$data}{diff}\n";
	    #	print REASON "\tdata : body : polarity = $om{$ent}{$file}{$data}{polarity}\n";
	    #	print REASON "\tdata : body : polarity_correct =  \n";
	    #	print REASON "\tdata : body : polarity_correct_which_word(s): \n";
	    #	  if ($om{$ent}{$file}{quant}{diff} =~ /[+]/) {
	    #	    $polarity = "34";
	    #	  }
	    #	  elsif ($om{$ent}{$file}{quant}{diff} =~ /[-]/) {
	    #	    $polarity = "01";
	    #	  }
	    #	  else {
	    #	    $polarity = "2"
	    #	  }

	   
	    #	  $pol = $om{$ent}{$file}{$data}{pol};
	    #	  print XML "<polarity>$polarity<\/polarity>\n";
	    if ($pol <= 4) {
	      $pol_total = $pol_total + $pol;
	      #	    print EXC "$ent\t\t$stock\t\t$source\t\t\t$day\.$month\.$year\t\t\$pol\t$text\n";
	      $n++;
	    }
	  }
	}
	print XML "<\/entity>\n"
      }
      if ($data eq 'quant') {
	#	print QUANT "\tdata : body : string = $om{$ent}{$file}{$data}{$sent}{string}\n";
	print QUANT "\tdata : title : hour = $om{$ent}{$file}{$data}{hour}\n";
	print QUANT "\tdata : title : minute = $om{$ent}{$file}{$data}{minute}\n";
	print QUANT "\tdata : body : quant = $om{$ent}{$file}{$data}{stock}\n";
	print QUANT "\tdata : body : diff = $om{$ent}{$file}{$data}{diff}\n";
	print QUANT "\tdata : body : polarity = $om{$ent}{$file}{$data}{polarity}\n";
	print QUANT "\tdata : body : polarity_correct =  \n";
	#	print QUANT "\tdata : body : polarity_correct_which_word(s): \n";
	$stock = $om{$ent}{$file}{$data}{stock};
	$pol = $om{$ent}{$file}{$data}{pol};
	if ($pol <= 4) {
	  $pol_total = $pol_total + $pol;
	  #	    print EXC "$ent\t\t$stock\t\t$source\t\t\t$day\.$month\.$year\t\t\$pol\t$text\n";
	  $n++;
	}
      }
	   
      #   print XML "<\/entity>\n";
    }
    if ($stock ne "") {
      $pol = "";
      $string = "";
      #      print EXC "$ent\t\t$stock\t\t$source\t\t$id\t\t\t$day\.$month\.$year\t\t$pol\t$string\n";
      print EXC "$ent\t\t$source\t\t$id\t\t\t$day\.$month\.$year\t\t$pol\t$string\n";
    } else {
      $pol_mean = $pol_total / $n;
      if ($pol_mean =~ /(\d+)\.(\d)\d*/) {
	if ($2 >= 5) {
	  $pol_mean = $1 + 1;
	} else {
	  $pol_mean = $1;
	}
      } 
      #      print EXC "$ent\t\t$stock\t\t$source\t\t$id\t\t\t$day\.$month\.$year\t\t$pol_total\t$string_total\n";
      print EXC "$ent\t\t$source\t\t$id\t\t\t$day\.$month\.$year\t\t$pol_total\t$string_total\n";
    }
    #    print XML "<\/mention>\n"; 
      
    $pol_total = 0;
    $string_total = ""; 
    $n = 1;
    $stock = "";
  }
}

print XML "<\/opinion>\n";

1; 

