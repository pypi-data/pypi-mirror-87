import argparse
import time
import hjson 
import traceback
from utilities import open_pickled_files

def run_vi_instance(hyper_params):

    import autograd.numpy.random as npr
    
    import interface
    from inference import  vi_on_stan_model

    print("Trying to load the model...")

    model = interface.get_logp([hyper_params['model_root_dir'], hyper_params['model_name']])

    print("Model successfully imported to autograd...")

    npr.seed(hyper_params['seed'])    #set up the seed and call the inference function 

    print("Starting Variational Inference...")

    vi_on_stan_model(model = model, hyper_params = hyper_params)

def run_vi(hyper_params):

    from utilities.result_helper import save_current_dict

    for exp in hyper_params['step_size_exp_range']:
    
        hyper_params['step_size_exp'] = exp
    
        try :
            print("Starting optimization...")

            start = time.time()

            run_vi_instance(hyper_params = hyper_params.copy())

            print("The time taken for the process : ",time.time() - start)
    
        except Exception:
    
            print(f"Error during the training of model {hyper_params['model_name']}...")

            print(traceback.print_exc())
    
    print(f"Optimization for {hyper_params['model_name']} done....")
    if "test" not in hyper_params['uniq_name']:
        save_current_dict(hyper_params = hyper_params)



if __name__ == "__main__" :
    

    parser = argparse.ArgumentParser()

    parser.add_argument('-uname', '--uname', type=str, required=True, 
        help="Unique name used for saving and retrieving.") 
    parser.add_argument('-ids', '--model_ids', type=int, required=False,
        help="Id of the models to experiment with. Should use Ids from table 1 in the paper.", nargs = "*") 
    parser.add_argument('-root', '--root_dir', type=str, required=False, 
        default = "./models",
        help="Root directory that contains the Stan code and the data for the model.") 
    parser.add_argument('-name', '--model_name', type=str, required=False, 
        help="Name of the model in the root directory. The same name is used to identify the Stan code and data files.") 
    parser.add_argument('-pconfig', '--pconfig', type=str, required=False, 
        default= '../ezstan/config.hjson', help="path to the .json config file")

    args = parser.parse_args()
    
    if args.pconfig:
        with open(args.pconfig, 'r') as f:
            hyper_params = hjson.load(f)
    else:
        raise NotImplementedError

    hyper_params['uniq_name'] = args.uname

    hyper_params['model_ids'] = args.model_ids


    
    if hyper_params['model_ids'] is None:
    
        assert args.model_name is not None
        assert args.root_dir is not None

        hyper_params['model_id'] = None
        hyper_params['model_root_dir'] = args.root_dir
        hyper_params['model_name'] = args.model_name

        run_vi(hyper_params)

    else: 

        model_orig_id_dict = (open_pickled_files("../data/utilities/good_model_new_id_to_old_id_dict.pkl"))
        model_names = (open_pickled_files("../data/utilities/good_model_name.pkl"))

        for m in hyper_params['model_ids']:

            hyper_params['model_id'] = model_orig_id_dict[m]
            hyper_params['model_root_dir'] = './models'
            hyper_params['model_name'] = model_names[hyper_params['model_id']]

            run_vi(hyper_params)
